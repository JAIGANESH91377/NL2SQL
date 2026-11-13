# 💡 NL2SQL Chatbot — Ask Your Database in Plain English

A chatbot that turns plain-English questions into SQL, runs them on a MySQL database and answers back in natural language. No SQL knowledge needed.

Built with **Gemini, LangChain, Chroma, Streamlit and MySQL**, with **Langfuse** tracing for every query.

---

## ✨ Features

- Converts natural-language questions into SQL automatically
- **Table selection by the LLM:** Gemini reads short descriptions of each table and picks the ones relevant to the question
- **Few-shot learning:** the most similar solved examples are retrieved by semantic similarity and added to the prompt
- **Follow-up questions:** chat history is passed into the prompt so the bot can handle follow-ups
- Runs the SQL on MySQL and explains the result in plain language
- **Langfuse tracing** of each run for logs and monitoring
- Simple chat interface built with Streamlit

## 🧠 How It Works

```
User question
     │
     ▼
Gemini picks relevant tables (using database_table_descriptions.csv)
     │
     ▼
Chroma + Gemini embeddings retrieve the top-2 similar few-shot examples
     │
     ▼
Prompt = table info + examples + chat history + question  ──►  Gemini writes SQL
     │
     ▼
SQL cleaned (regex) and executed on MySQL (LIMIT applied)
     │
     ▼
Gemini turns the result into a plain-language answer
     │
     ▼
Shown in the Streamlit chat · traced in Langfuse
```

## 🛠️ Tech Stack

- **Language:** Python
- **LLM:** Google Gemini (`gemini-1.5-flash`) via `langchain-google-genai`
- **Framework:** LangChain
- **Vector store / embeddings:** Chroma with Gemini `embedding-001`
- **Database:** MySQL (PyMySQL), sample `classicmodels` database
- **UI:** Streamlit
- **Monitoring:** Langfuse

## 📁 Project Structure

```
├── main.py                              # Streamlit chat interface
├── langchain_utils.py                   # Chain: table selection, SQL generation, execution, answer, Langfuse
├── examples.py                          # Few-shot examples and semantic example selector (Chroma)
├── prompts.py                           # Few-shot and chat-history prompt templates
├── table_details.py                     # Loads table descriptions
├── database_table_descriptions.csv      # Short description of each table (used for table selection)
├── requirements.txt
├── .env.example                         # Template for your secrets (the real .env is NOT committed)
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JAIGANESH91377/<your-repo-name>.git
cd <your-repo-name>
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

Load the `classicmodels` sample database into a local MySQL server.

### 5. Create a `.env` file (copy `.env.example`)

```env
db_user=your_mysql_username
db_password=your_mysql_password
db_host=localhost
db_name=classicmodels

GOOGLE_API_KEY=your_gemini_api_key

LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

> 🔒 Never commit your `.env` file. Keep it listed in `.gitignore`.

### 6. Run the app

```bash
streamlit run main.py
```

Open the local URL shown in the terminal (usually http://localhost:8501).

## 💬 Example

**You:** What is the price of 1969 Harley Davidson Ultimate Chopper?

**Generated SQL:**
```sql
SELECT MSRP FROM products WHERE productName = '1969 Harley Davidson Ultimate Chopper';
```

**Answer:** The price of the 1969 Harley Davidson Ultimate Chopper is $95.70.

## ⚠️ Known Limitations

- Complex multi-table joins and ambiguous questions can produce wrong SQL.
- Only 5 few-shot examples are used.
- Generated SQL is executed as-is, so connect with a **read-only database user**.

## 🔭 Future Improvements

- Validate generated SQL before running it, and enforce read-only access
- A larger, more varied example set
- Support for more databases (PostgreSQL, MongoDB)
- Charts and visualisation of query results

## 👤 Author

**Jaiganesh Mabbu**
AI & Data Science graduate — Python, SQL, Machine Learning, Generative AI

- 🌐 [Portfolio](https://jaiganesh-portfolio.vercel.app/)
- 💼 [LinkedIn](https://www.linkedin.com/in/jaiganesh-mabbu-69720323a/)
- 🐙 [GitHub](https://github.com/JAIGANESH91377)
- 📧 [Gmail](mailto:3227jaiganeshmabbu@gmail.com)
