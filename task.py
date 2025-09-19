from tools import FinancialDocumentTool
from agents import financial_analyst
import os, uuid, json, threading
from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "analysis.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String)
    status = Column(String)
    result = Column(Text)  # JSON string

Base.metadata.create_all(bind=engine)

def _save_result_to_db(analysis_id: str, filename: str, result: dict):
    session = SessionLocal()
    try:
        a = session.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not a:
            a = Analysis(id=analysis_id, filename=filename, status="done", result=json.dumps(result))
            session.add(a)
        else:
            a.status = "done"
            a.result = json.dumps(result)
        session.commit()
    finally:
        session.close()

def analyze_financial_document(file_path: str, original_filename: str = None) -> dict:
    text = FinancialDocumentTool.read_data(file_path)
    analysis = financial_analyst(text)
    metadata = {}
    try:
        metadata["file_size_bytes"] = os.path.getsize(file_path)
        metadata["file_name"] = original_filename or os.path.basename(file_path)
    except Exception:
        pass
    return {"metadata": metadata, "analysis": analysis}

def _background_worker(analysis_id: str, file_path: str, orig_filename: str):
    try:
        result = analyze_financial_document(file_path, original_filename=orig_filename)
        _save_result_to_db(analysis_id, orig_filename or os.path.basename(file_path), result)
    except Exception as e:
        session = SessionLocal()
        a = session.query(Analysis).filter(Analysis.id == analysis_id).first()
        if a:
            a.status = "error"
            a.result = json.dumps({"error": str(e)})
            session.commit()
        session.close()
    finally:
        try:
            os.remove(file_path)
        except Exception:
            pass

def enqueue_analysis(file_path: str, orig_filename: str = None) -> str:
    analysis_id = str(uuid.uuid4())
    session = SessionLocal()
    try:
        a = Analysis(id=analysis_id, filename=orig_filename or os.path.basename(file_path), status="processing", result="")
        session.add(a)
        session.commit()
    finally:
        session.close()
    t = threading.Thread(target=_background_worker, args=(analysis_id, file_path, orig_filename), daemon=True)
    t.start()
    return analysis_id

def get_analysis(analysis_id: str):
    session = SessionLocal()
    try:
        a = session.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not a:
            return None
        if a.status != "done":
            return None
        try:
            return json.loads(a.result)
        except:
            return {"raw": a.result}
    finally:
        session.close()
