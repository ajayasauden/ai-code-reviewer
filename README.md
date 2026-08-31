#  AI Engineering Multi-Tool Suite

An end-to-end Python application suite combining CLI tools, REST APIs, and an interactive Streamlit frontend. Powered by **Google Gemini API**, **FastAPI**, **Pandas**, and **PyPDF**.

---

##  Key Features

* ** AI Code Reviewer (`reviewer.py` & `main.py`)**: Analyzes Python code snippets, identifies bugs, suggests PEP 8 style fixes, and assigns quality scores. Available as both a CLI tool with Markdown export and a REST API.
* ** CSV Data Summarizer (`data_summarizer.py`)**: Uses Pandas to extract statistical overviews of tabular datasets and generates AI executive summaries.
* ** Document Query Engine (`doc_query.py`)**: Parses PDF and text files using `pypdf` to answer questions directly against local context.
* ** Interactive Web Dashboard (`app.py`)**: A Streamlit frontend unifying the suite into a multi-tab web application.

---

## 🛠️ Tech Stack & Dependencies

* **Language**: Python 3.10+
* **AI Model**: Google Gemini API (`google-genai`)
* **Backend Framework**: FastAPI & Uvicorn
* **Data Processing**: Pandas, PyPDF
* **Frontend**: Streamlit
* **Environment Management**: `python-dotenv`

---

##  Quickstart Guide

### 1. Clone & Set Up Environment
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt