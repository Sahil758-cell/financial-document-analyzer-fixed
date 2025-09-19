# 📊 Financial Document Analyzer – Debug Assignment (Fixed)

This project started as a **buggy assignment repo**.  
I debugged it, fixed the broken code, and added new functionality so it’s now a working **Financial Document Analyzer API** built with **FastAPI**.

---

## 🚀 Features
- Accepts **PDF** or **TXT** documents.
- Extracts text (using `PyPDF2`).
- Performs **rule-based analysis**:
  - Generates a quick **summary**.
  - Extracts **key figures** (Revenue, Net Income, EPS, etc.).
  - Computes simple **metrics** (profit margin).
  - Provides a **recommendation** (positive / neutral / negative).
- Two modes of analysis:
  - **Sync** → `/analyze_sync` → immediate results.
  - **Async** → `/analyze` → enqueues job, fetch later with `/analysis/{id}`.
- Persists results in **SQLite** (`analysis.db`).
- Interactive **Swagger UI** at `/docs`.

---

## 🐞 Bugs Found & Fixes

| File | Bug(s) Found | Fix Applied |
|------|--------------|-------------|
| `agents.py` | `llm = llm` (undefined), CrewAI agents hallucinated responses | Replaced with a **deterministic rule-based analyzer** (`financial_analyst`). |
| `tools.py` | Used `Pdf` (nonexistent), no real text extraction | Replaced with **`PyPDF2.PdfReader`**, added error handling. |
| `task.py` | CrewAI tasks with nonsense prompts, no persistence | Implemented `analyze_financial_document()`, added **background worker** + **SQLite DB**. |
| `main.py` | Broken endpoints, invalid imports, no root health check | Rebuilt with **FastAPI endpoints**: `/analyze`, `/analyze_sync`, `/analysis/{id}`. |
| `requirements.txt` | Overly complex, conflicting pinned versions | Replaced with a **minimal requirements list** that installs cleanly. |

---

## 🛠️ Setup Instructions

### 1. Clone & Setup
```bash
git clone https://github.com/<your-username>/financial-document-analyzer-fixed.git
cd financial-document-analyzer-fixed

python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
2. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt

3. Run the Server
uvicorn main:app --reload --port 8000

4. Open Swagger UI

Visit → http://127.0.0.1:8000/docs

🔥 API Documentation
POST /analyze_sync

Upload a PDF/TXT → get result immediately.

curl -F "file=@data/TSLA-Q2-2025-Update.pdf" http://127.0.0.1:8000/analyze_sync


Example Response:

{
  "status": "ok",
  "result": {
    "metadata": {
      "file_size_bytes": 9489744,
      "file_name": "TSLA-Q2-2025-Update.pdf"
    },
    "analysis": {
      "summary": "Tesla reported revenue ...",
      "key_figures": {
        "revenue": "$25,000,000",
        "net_income": "$3,200,000"
      },
      "metrics": {
        "profit_margin": 0.128
      },
      "recommendation": "neutral"
    }
  }
}

POST /analyze

Upload file

Returns analysis_id

Job runs in background

GET /analysis/{analysis_id}

Fetch result when job finishes

🧪 Run Tests
pytest -q

📦 Tech Stack

FastAPI – API framework

PyPDF2 – PDF text extraction

SQLAlchemy + SQLite – data persistence

pytest – testing

📌 Notes

Current analysis is rule-based, not hallucinations.

For production:

Replace thread-based queue with Celery + Redis.

Use pdfminer.six for better PDF parsing.

🙋 Author

Debugged and implemented by Sahil Surendra Deshmukh
📧 Email: sahidesh02@gmail.com
