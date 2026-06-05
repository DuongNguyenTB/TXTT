from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List
from openai import OpenAI

# 1. IMPORT LOGIC TỪ FILE rag_logic.py
from rag_logic import process_and_store_document, retrieve_context

app = FastAPI()

# ==========================================
# CẤU HÌNH API VÀ LLM
# ==========================================
STUDENT_ID = "MÃ_SINH_VIÊN_CỦA_BẠN"  # Nhớ đổi mã SV viết hoa
TEACHER_SERVER_IP = "192.168.50.218" # Kiểm tra lại IP lúc vào thi
PROXY_BASE_URL = f"http://{TEACHER_SERVER_IP}:8000/api/v1/proxy"

# Khởi tạo client gọi Proxy LLM
client = OpenAI(
    base_url=PROXY_BASE_URL,
    api_key=STUDENT_ID
)

# ==========================================
# SCHEMA (Bắt buộc phải khớp với slide)
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
    sources: List[str] = []

# ==========================================
# ENDPOINTS
# ==========================================

@app.post("/upload", response_model=UploadResponse)
async def upload_document(req: UploadRequest):
    """
    Endpoint 1: Nhận tài liệu từ Teacher Server, thực hiện Chunking và lưu vào VectorDB.
    Thời gian tối đa: 120s
    """
    try:
        # Gọi hàm xử lý chunking và lưu vào FAISS từ rag_logic.py
        chunks_created = process_and_store_document(req.text)
        
        return UploadResponse(
            status="success",
            doc_id=req.doc_id,
            chunks=chunks_created
        )
    except Exception as e:
        print(f"Lỗi khi upload và xử lý chunk: {e}")
        return UploadResponse(
            status="error",
            doc_id=req.doc_id,
            chunks=0
        )

@app.post("/ask", response_model=AskResponse)
async def ask_question(req: AskRequest):
    """
    Endpoint 2: Nhận câu hỏi, RAG và trả về đúng 1 ký tự A/B/C/D.
    Thời gian tối đa: 60s
    """
    # 1. Query VectorDB để lấy Context thực tế từ hàm retrieve_context
    retrieved_context, retrieved_sources = retrieve_context(req.question, top_k=3)
    
    # 2. Tạo Prompt (Giới hạn Proxy LLM khoảng 2048-4096 tokens nên prompt cần gọn gàng)
    system_prompt = (
        "Bạn là một trợ lý ảo giải trắc nghiệm. "
        "Dựa vào Context được cung cấp, hãy trả lời câu hỏi của người dùng. "
        "CHỈ TRẢ VỀ ĐÚNG 1 KÝ TỰ là đáp án đúng: A, B, C, hoặc D. Không giải thích thêm."
    )
    
    user_prompt = f"Context:\n{retrieved_context}\n\nQuestion:\n{req.question}"
    
    # 3. Gọi LLM qua Proxy
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        # 4. Tiền xử lý đáp án (Đảm bảo nó chỉ có 1 ký tự A/B/C/D)
        raw_answer = response.choices[0].message.content.strip().upper()
        # Lọc ra ký tự A, B, C, D đầu tiên xuất hiện
        final_answer = next((char for char in raw_answer if char in ['A', 'B', 'C', 'D']), 'A')
        
    except Exception as e:
        print(f"Lỗi gọi LLM: {e}")
        final_answer = "A" # Trả về bừa 1 đáp án để tránh rớt request
        
    return AskResponse(
        answer=final_answer,
        sources=retrieved_sources
    )

# Chạy server bằng: uvicorn main:app --host 0.0.0.0 --port 5000