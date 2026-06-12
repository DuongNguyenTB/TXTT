import os  # <-- ĐÃ SỬA: Thêm thư viện os để kiểm tra file
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

# ==========================================
# CẤU HÌNH OFFLINE EMBEDDING
# ==========================================
MODEL_PATH = "./models/vietnamese-sbert-base"  # <-- ĐÃ SỬA: Đường dẫn đến model embedding đã tải về máy
FAISS_DB_DIR = "./faiss_index"  # <-- ĐÃ SỬA: Khai báo thư mục lưu VectorDB xuống ổ cứng

print("Đang load model embedding offline...")
try:
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_PATH)
    print(" Load model thành công!")
except Exception as e:
    print(f" Lỗi load model (Có thể bạn chưa tải model về máy): {e}")

# Biến toàn cục để lưu trữ VectorDB trên RAM
vector_db = None

def load_existing_db():
    global vector_db
    if os.path.exists(FAISS_DB_DIR):
        # allow_dangerous_deserialization=True là bắt buộc ở các bản Langchain mới khi load local FAISS
        vector_db = FAISS.load_local(FAISS_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print(" Đã load VectorDB thành công từ ổ cứng!")
    else:
        print(" Chưa có VectorDB trên ổ cứng. Cần nhận tài liệu từ Teacher Server.")

def process_and_store_document(text: str) -> int:
    global vector_db
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks_text = text_splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks_text]
    
    vector_db = FAISS.from_documents(documents, embeddings)
    
    # THÊM DÒNG NÀY: Lưu thẳng xuống ổ cứng sau khi embed xong
    vector_db.save_local(FAISS_DB_DIR) 
    print(" Đã lưu VectorDB xuống ổ cứng an toàn!")
    
    return len(chunks_text)

def retrieve_context(question: str, top_k: int = 3) -> tuple[str, list[str]]:
    """
    Tìm kiếm k đoạn văn bản có ngữ cảnh gần giống nhất với câu hỏi.
    """
    global vector_db
    if vector_db is None:
        return "Không có dữ liệu trong VectorDB.", []
    
    # Tìm kiếm độ tương đồng (Similarity Search)
    matched_docs = vector_db.similarity_search(question, k=top_k)
    
    # Nối các đoạn văn bản tìm được lại với nhau để làm Context cho LLM
    context_text = "\n---\n".join([doc.page_content for doc in matched_docs])
    
    # (Tùy chọn) Giả lập ID cho source
    sources = [f"chunk_{i}" for i in range(len(matched_docs))]
    
    return context_text, sources