from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

# ==========================================
# CẤU HÌNH OFFLINE EMBEDDING
# ==========================================
# LƯU Ý QUAN TRỌNG: Bạn BẮT BUỘC phải tải folder model này về máy trước khi bị ngắt mạng!
# Bạn có thể dùng script Python đơn giản bằng huggingface_hub để tải model "sentence-transformers/all-MiniLM-L6-v2" về thư mục "./models".
MODEL_PATH = "./models/all-MiniLM-L6-v2" 

print("Đang load model embedding offline...")
try:
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_PATH)
    print("Load model thành công!")
except Exception as e:
    print(f"Lỗi load model (Có thể bạn chưa tải model về máy): {e}")

# Biến toàn cục để lưu trữ VectorDB trên RAM
vector_db = None

def process_and_store_document(text: str) -> int:
    """
    Thực hiện Chunking và lưu vào FAISS VectorDB.
    """
    global vector_db
    
    # 1. CHUNKING: Cắt văn bản thành các đoạn nhỏ
    # chunk_size: Kích thước mỗi đoạn (ký tự). 
    # chunk_overlap: Số ký tự trùng lặp giữa 2 đoạn liên tiếp để giữ ngữ cảnh.
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    # Cắt text gốc ra thành một list các chuỗi
    chunks_text = text_splitter.split_text(text)
    
    # Ép kiểu về dạng Document của Langchain
    documents = [Document(page_content=chunk) for chunk in chunks_text]
    
    # 2. VECTOR DB: Nhúng (Embed) các chunk và lưu vào FAISS
    # Mỗi lần /upload gọi, ta sẽ tạo lại DB mới (hoặc bạn có thể dùng vector_db.add_documents nếu muốn cộng dồn)
    vector_db = FAISS.from_documents(documents, embeddings)
    
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