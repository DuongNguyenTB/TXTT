import os
from typing import Any, List, Optional
from fastapi import FastAPI, Request
from openai import OpenAI
from pydantic import BaseModel, Field

# IMPORT LOGIC TU FILE rag_logic.py
from rag_logic import process_and_store_document, retrieve_context, load_existing_db

app = FastAPI()

# Nap database tu o cung ngay khi khoi dong
load_existing_db()

# ==========================================
# CAU HINH API VA LLM
# ==========================================
STUDENT_ID = os.getenv("STUDENT_ID", "B21DCCNxxx").strip().upper()
TEACHER_SERVER_IP = os.getenv("TEACHER_SERVER_IP", "192.168.50.218").strip()
PROXY_BASE_URL = f"http://{TEACHER_SERVER_IP}:8000/api/v1/proxy"

client = OpenAI(base_url=PROXY_BASE_URL, api_key=STUDENT_ID, timeout=45.0)

# ==========================================
# SCHEMA
# ==========================================
class UploadRequest(BaseModel):
    doc_id: Optional[str] = None
    text: str

class UploadResponse(BaseModel):
    status: str
    doc_id: Optional[str] = None
    chunks: int

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    sources: List[str] = Field(default_factory=list)

# ==========================================
# HAM BO TRO DE CHONG LOI INPUT
# ==========================================
def _extract_text(payload: Any) -> str:
    if isinstance(payload, str): return payload.strip()
    if isinstance(payload, dict):
        return str(payload.get("text", "")).strip()
    return ""

def _normalize_answer(raw_answer: str) -> str:
    cleaned = (raw_answer or "").strip().upper()
    return next((char for char in cleaned if char in {"A", "B", "C", "D"}), "A")

# ==========================================
# ENDPOINTS
# ==========================================

@app.post("/upload", response_model=UploadResponse)
async def upload_document(request: Request):
    """Nhan tai lieu linh hoat de chong loi 422"""
    try:
        data = await request.json()
        doc_id = data.get("doc_id")
        text = _extract_text(data)
        
        chunks_created = process_and_store_document(text, doc_id=doc_id)
        return UploadResponse(status="success", doc_id=doc_id, chunks=chunks_created)
    except Exception as e:
        print(f"Loi upload: {e}")
        return UploadResponse(status="error", doc_id=None, chunks=0)

@app.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    """Nhan cau hoi, truy xuat ngu canh va tra loi A/B/C/D"""
    retrieved_context, retrieved_sources = retrieve_context(req.question, top_k=3)
    
    system_prompt = (
        "Ban la tro ly giai trac nghiem. Dua vao Context, tra loi cau hoi. "
        "CHI TRA VE DUNG 1 KY TU: A, B, C, hoac D. Khong giai thich."
    )
    user_prompt = f"Context:\n{retrieved_context}\n\nQuestion:\n{req.question}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        raw_answer = response.choices[0].message.content or ""
        final_answer = _normalize_answer(raw_answer)
    except Exception as e:
        print(f"Loi LLM: {e}")
        final_answer = "A"
        
    return AskResponse(answer=final_answer, sources=retrieved_sources)