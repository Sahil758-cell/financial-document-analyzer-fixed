from fastapi import FastAPI, File, UploadFile, HTTPException
import os, uuid
from task import analyze_financial_document, enqueue_analysis, get_analysis

app = FastAPI(title="Financial Document Analyzer")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".txt"):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")
    uid = str(uuid.uuid4())
    dest = os.path.join(UPLOAD_DIR, f"{uid}{ext}")
    with open(dest, "wb") as f:
        f.write(await file.read())
    # enqueue background analysis and return an id
    analysis_id = enqueue_analysis(dest, file.filename)
    return {"status": "accepted", "analysis_id": analysis_id, "note": "Analysis runs in background. Use /analysis/{id} to fetch result."}

@app.get("/analysis/{analysis_id}")
def read_analysis(analysis_id: str):
    res = get_analysis(analysis_id)
    if not res:
        raise HTTPException(status_code=404, detail="Analysis not found yet or still processing")
    return {"status": "done", "result": res}

@app.post("/analyze_sync")
async def analyze_sync(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".txt"):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported.")
    uid = str(uuid.uuid4())
    dest = os.path.join(UPLOAD_DIR, f"{uid}{ext}")
    with open(dest, "wb") as f:
        f.write(await file.read())
    try:
        result = analyze_financial_document(dest, original_filename=file.filename)
        return {"status": "ok", "result": result}
    finally:
        try:
            os.remove(dest)
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
