import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings


import asyncio
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())


# -------------------------------
# Load environment variables
# -------------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_URI = os.getenv("DB_URI") or f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

if not DB_URI:
    raise ValueError("⚠️ Missing DB_URI in .env file")

# -------------------------------
# Connect to Database
# -------------------------------
db = SQLDatabase.from_uri(DB_URI)
print("✅ Connected to DB. Tables available:", db.get_usable_table_names())

# -------------------------------
# Initialize Gemini LLM
# -------------------------------
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# -------------------------------
# Few-Shot Examples
# -------------------------------
FEW_SHOT_EXAMPLES = [
    {"question": "List names of customers in France", "sql": "SELECT customerName FROM customers WHERE country='France';"},
    {"question": "What is price of `1969 Harley Davidson Ultimate Chopper`?", "sql": "SELECT MSRP FROM products WHERE productName='1969 Harley Davidson Ultimate Chopper';"},
    {"question": "How many customers have an order count greater than 5?", "sql": "SELECT COUNT(*) FROM customers WHERE customerNumber IN (SELECT customerNumber FROM orders GROUP BY customerNumber HAVING COUNT(*) > 5);"},
    {"question": "What is the average salary of Sales Reps?", "sql": "SELECT AVG(salary) FROM employees WHERE jobTitle='Sales Rep';"},
    {"question": "Who reports to the President?", "sql": "SELECT firstName, lastName FROM employees WHERE reportsTo IN (SELECT employeeNumber FROM employees WHERE jobTitle='President');"}
]

# -------------------------------
# ✅ Local Embedding Model (No API, No Quota)
# -------------------------------
# You can change the model if you like — this one is fast and accurate.
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Build FAISS vector store
docs = [ex["question"] for ex in FEW_SHOT_EXAMPLES]
metadatas = [{"sql": ex["sql"]} for ex in FEW_SHOT_EXAMPLES]
vectorstore = FAISS.from_texts(docs, embeddings, metadatas=metadatas)

def get_relevant_examples(query, k=2):
    """Retrieve top-k relevant few-shot examples"""
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join([f"Q: {r.page_content}\nSQL: {r.metadata['sql']}" for r in results])

# -------------------------------
# Dynamic Table Selection
# -------------------------------
def get_relevant_tables(question, top_k=3):
    """Select relevant tables based on keywords in the question"""
    tables = db.get_usable_table_names()
    relevant = [t for t in tables if t.lower() in question.lower()]
    if not relevant:
        relevant = tables  # fallback if no keyword match
    return relevant[:top_k]

# -------------------------------
# SQL Query Prompt with Few-Shot + Dynamic Schema
# -------------------------------
def build_dynamic_prompt(question):
    tables = get_relevant_tables(question)
    schema = db.get_table_info(tables)
    examples = get_relevant_examples(question)
    return (
        f"You are a helpful assistant that writes SQL queries.\n"
        f"Schema (only relevant tables):\n{schema}\n\n"
        f"Relevant examples:\n{examples}\n\n"
        f"Now write a SQL query for this question:\n{question}\n"
        "Return ONLY the SQL query."
    )

# -------------------------------
# Chain Components
# -------------------------------
def extract_sql(output):
    text = output.content if hasattr(output, "content") else str(output)
    return text.replace("```sql", "").replace("```", "").strip()

generate_query = RunnableLambda(lambda x: llm.invoke(build_dynamic_prompt(x["question"])))
sql_extractor = RunnableLambda(lambda x: extract_sql(x["query"]))
execute_sql = RunnableLambda(lambda sql: db.run(sql))

answer_prompt = PromptTemplate(
    input_variables=["question", "result"],
    template="Question: {question}\n\nSQL Result: {result}\n\nAnswer the question using only this result."
)
answer_chain = answer_prompt | llm

# -------------------------------
# Full pipeline
# -------------------------------
chain = (
    RunnablePassthrough.assign(query=generate_query)
    | RunnablePassthrough.assign(sql=sql_extractor)
    | RunnablePassthrough.assign(result=lambda x: execute_sql.invoke(x["sql"]))
    | RunnablePassthrough.assign(answer=lambda x: answer_chain.invoke({
        "question": x["question"],
        "result": x["result"]
    }))
)
