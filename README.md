# 💡 Natural Language to SQL Chatbot (Gemini + FAISS + Streamlit)

Ask questions about a MySQL database in plain English. The app writes the SQL, runs it, and answers back in natural language.

This version uses **local embeddings with FAISS** for few-shot example retrieval, so retrieval needs no API quota.

---

## ✨ Features

- Converts natural-language questions into SQL automatically
- Runs the query on a connected MySQL database
- Replies in an easy-to-read conversational answer
- **FAISS few-shot retrieval:** finds the most similar solved examples and adds them to the prompt
- **Local embeddings** (`all-MiniLM-L6-v2`): no embedding API calls or quota
- **Dynamic table selection:** only the relevant table schemas are sent to the model
- Simple chat interface built with Streamlit

## 🧠 How It Works

```
User question
     │
     ▼
Select relevant tables (keyword match on table names; falls back to the first 3 tables)
     │
     ▼
FAISS retrieves the top-2 most similar few-shot examples
(local all-MiniLM-L6-v2 embeddings, 5 stored examples)
     │
     ▼
Prompt = table schema + examples + question  ──►  Gemini (gemini-pro) writes SQL
     │
     ▼
SQL cleaned of markdown fences and executed on MySQL
     │
     ▼
Gemini answers the question using only the SQL result
     │
     ▼
Displayed in the Streamlit chat
```

## 🛠️ Tech Stack

- **Python 3.10+**
- **Google Gemini** (`gemini-pro`) via `langchain-google-genai`
- **LangChain**
- **FAISS** (vector search)
- **HuggingFace sentence-transformers** (`all-MiniLM-L6-v2`, runs locally)
- **MySQL** with PyMySQL
- **Streamlit**

## 📁 Project Structure

```
├── final_int_env.py          # Pipeline: DB connection, FAISS few-shot retrieval, table selection, SQL generation, execution, answer
├── final_intapp.py           # Streamlit chat interface
├── requirements.txt          # Dependencies
├── .env.example              # Template for your secrets (the real .env is NOT committed)
└── README.md
```

## 🚀 Setup

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

### 4. Create a `.env` file

```env
DB_USER=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_NAME=your_database_name
# Optional: use one connection string instead of the four values above
# DB_URI=mysql+pymysql://your_mysql_username:your_mysql_password@localhost/your_database_name

GOOGLE_API_KEY=your_gemini_api_key
```

> 🔒 Never commit your `.env` file. Keep it listed in `.gitignore`.

### 5. Run the app

```bash
streamlit run final_intapp.py
```

Open the local URL shown in the terminal (usually http://localhost:8501) and ask a question.

## 💬 Examples

**You:** List names of customers in France.

**Answer:** The customers in France are Atelier graphique, La Rochelle Gifts, and Mini Gifts Distributors Ltd.

---

**You:** What is the price of 1969 Harley Davidson Ultimate Chopper?

**Generated SQL:**
```sql
SELECT MSRP FROM products WHERE productName = '1969 Harley Davidson Ultimate Chopper';
```

**Answer:** The price of the 1969 Harley Davidson Ultimate Chopper is $95.70.

## ⚠️ Known Limitations

- Table selection is keyword-based, so complex multi-table joins and ambiguous questions can fail.
- Each question is handled on its own, so follow-up questions are not understood.
- Only 5 few-shot examples are stored.
- Generated SQL is executed as-is, so connect with a **read-only database user**.

## 🔭 Future Improvements

- Embedding-based or LLM-based table selection
- Conversation memory for multi-turn questions
- Query logging and monitoring with Langfuse
- Validation of generated SQL before execution
- Support for more databases (PostgreSQL, MongoDB) and result visualisation

## 👤 Author

**Jaiganesh Mabbu**
AI & Data Science graduate — Python, SQL, Machine Learning, Generative AI

- 🌐 [Portfolio](https://jaiganesh-portfolio.vercel.app/)
- 💼 [LinkedIn](https://www.linkedin.com/in/jaiganesh-mabbu-69720323a/)
- 🐙 [GitHub](https://github.com/JAIGANESH91377)
- 📧 [3227jaiganeshmabbu@gmail.com](mailto:3227jaiganeshmabbu@gmail.com)
