
import os, re

class FinancialDocumentTool:
    @staticmethod
    def read_data(file_path: str) -> str:
        """
        Read text content from supported files.
        For .txt files, return text. For .pdf, we attempt a very small, dependency-free heuristic:
        return a note that PDF text extraction requires PyPDF2 or similar. The app will still work and report file metadata.
        """
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        if ext == ".txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        elif ext == ".pdf":
            # return a placeholder; proper extraction needs PyPDF2 or pdfminer.six
            try:
                size = os.path.getsize(file_path)
                return f"[PDF_BINARY_CONTENT] (size_bytes={size}). Text extraction not available in simplified build."
            except Exception as e:
                return f"[PDF_BINARY_CONTENT] (error reading file: {e})"
        else:
            raise ValueError("Unsupported file type: " + ext)
