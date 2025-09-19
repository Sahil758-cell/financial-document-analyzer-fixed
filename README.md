Financial Document Analyzer (Debug Assignment – Fixed Version)

This project started as a buggy assignment repo. I debugged it, fixed the broken code, and added new functionality so it’s now a working Financial Document Analyzer API built with FastAPI.
What This Project Does
- Accepts PDF or TXT financial documents.
- Extracts text (using PyPDF2).
- Runs a rule-based analysis:
   • Generates a quick summary of the document.
   • Extracts key financial figures (Revenue, Net Income, EPS, etc).
   • Computes simple metrics like profit margin.
   • Provides a basic recommendation (positive / neutral / negative).
- Supports two modes:
   • Sync analysis → /analyze_sync → immediate result.
   • Async analysis → /analyze → enqueues background job → fetch with /analysis/{id}.
- Stores results in a lightweight SQLite database (analysis.db).
- Provides an interactive Swagger UI at /docs.
Original Problems (Bugs) & How I Fixed Them
File	Bug(s) Found	Fix Applied
agents.py	llm = llm (undefined), agents gave nonsense/hallucinations	Removed fake CrewAI agents and replaced with a deterministic rule-based analyzer (financial_analyst).
tools.py	Used Pdf (nonexistent class), no actual text extraction	Replaced with PyPDF2.PdfReader for real PDF text extraction. Added fallback error handling.
task.py	Tasks used CrewAI/Agents with hallucination prompts, no persistence	Replaced with real analyze_financial_document() function. Added background worker and SQLite DB.
main.py	Endpoints broken, wrong CrewAI imports, no health check	Rebuilt API with FastAPI: /analyze, /analyze_sync, /analysis/{id}.
requirements.txt	Overly complex, pinned wrong versions, install conflicts	Created a minimal requirements.txt that installs cleanly and supports all features.

Setup Instructions
1. Clone & Setup
git clone https://github.com/<your-username>/financial-document-analyzer-fixed.git
cd financial-document-analyzer-fixed

python -m venv .venv
.venv\Scripts\activate   (Windows)
source .venv/bin/activate  (Linux/Mac)
2. Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt
3. Run the Server
uvicorn main:app --reload --port 8000
4. Open Swagger UI at http://127.0.0.1:8000/docs
API Documentation
POST /analyze_sync → Upload a PDF or TXT and get results immediately.
POST /analyze → Upload a file, returns an analysis_id, processes in background.
GET /analysis/{id} → Fetch results for a queued analysis.
Example curl:
curl -F "file=@data/TSLA-Q2-2025-Update.pdf" http://127.0.0.1:8000/analyze_sync
Running Tests
pytest -q
Tech Stack
- FastAPI
- PyPDF2
- SQLAlchemy + SQLite
- pytest
Notes
- Current analysis is rule-based (not AI hallucinations).
- For production, async queue can be upgraded to Celery + Redis.
- For richer PDF parsing, swap PyPDF2 with pdfminer.six.
Author
Debugged and implemented by Sahil Surendra Deshmukh
Email:sahidesh02@gmail.com
