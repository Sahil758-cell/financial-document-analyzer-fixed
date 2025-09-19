import os, re

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF using PyPDF2. Returns an error string if extraction fails."""
    try:
        from PyPDF2 import PdfReader
    except Exception as e:
        return f"[PDF_EXTRACTION_ERROR: missing PyPDF2: {e}]"
    try:
        reader = PdfReader(file_path)
        pages = []
        for p in reader.pages:
            txt = p.extract_text()
            if txt:
                pages.append(txt)
        return "\n".join(pages).strip()
    except Exception as e:
        return f"[PDF_EXTRACTION_ERROR: {e}]"

class FinancialDocumentTool:
    @staticmethod
    def read_data(file_path: str) -> str:
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf":
            return extract_text_from_pdf(file_path)
        else:
            raise ValueError("Unsupported file type: " + ext)
