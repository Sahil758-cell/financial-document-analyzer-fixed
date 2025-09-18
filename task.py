
from tools import FinancialDocumentTool
from agents import financial_analyst

def analyze_financial_document(file_path: str) -> dict:
    """
    High-level orchestration: read document, run simple analysis, return structured result.
    """
    text = FinancialDocumentTool.read_data(file_path)
    analysis = financial_analyst(text)
    metadata = {}
    try:
        import os
        metadata["file_size_bytes"] = os.path.getsize(file_path)
        metadata["file_name"] = os.path.basename(file_path)
    except Exception:
        pass
    return {"metadata": metadata, "analysis": analysis}
