
from fastapi import FastAPI, File, UploadFile, HTTPException
import os, uuid, shutil
from task import analyze_financial_document

app = FastAPI(title="Financial Document Analyzer (simplified)")

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # Save uploaded file
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".txt"):
        raise HTTPException(status_code=400, detail="Only .pdf and .txt files are supported in this simplified version.")
    uid = str(uuid.uuid4())
    dest = os.path.join(UPLOAD_DIR, f"{uid}{ext}")
    with open(dest, "wb") as f:
        content = await file.read()
        f.write(content)
    try:
        result = analyze_financial_document(dest)
        return {"status": "ok", "result": result}
    finally:
        try:
            os.remove(dest)
        except Exception:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
