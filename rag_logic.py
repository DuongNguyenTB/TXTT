import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

# ==========================================
# CAU HINH OFFLINE EMBEDDING
# ==========================================
MODEL_PATH = "./models/vietnamese-sbert-base" 
FAISS_DB_DIR = "./faiss_index"

print("Dang load model embedding offline...")
try:
    embeddings = HuggingFaceEmbeddings(model_name=MODEL_PATH)
    print("Load model thanh cong!")
except Exception as e:
    print(f"Loi load model: {e}")

vector_db = None

def load_existing_db():
    global vector_db
    if os.path.exists(FAISS_DB_DIR):
        vector_db = FAISS.load_local(FAISS_DB_DIR, embeddings, allow_dangerous_deserialization=True)
        print("Da load VectorDB thanh cong tu o cung!")
    else:
        print("Chua co VectorDB tren o cung.")

# DA SUA: Them doc_id vao tham so de khop voi main.py
def process_and_store_document(text: str, doc_id: str | None = None) -> int:
    global vector_db
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks_text = text_splitter.split_text(text)
    documents = [Document(page_content=chunk) for chunk in chunks_text]
    
    vector_db = FAISS.from_documents(documents, embeddings)
    
    # Luu xuong o cung
    vector_db.save_local(FAISS_DB_DIR) 
    print("Da luu VectorDB xuong o cung an toan!")
    
    return len(chunks_text)

def retrieve_context(question: str, top_k: int = 3) -> tuple[str, list[str]]:
    global vector_db
    if vector_db is None:
        return "Khong co du lieu trong VectorDB.", []
    
    matched_docs = vector_db.similarity_search(question, k=top_k)
    context_text = "\n---\n".join([doc.page_content for doc in matched_docs])
    
    sources = [f"chunk_{i}" for i in range(len(matched_docs))]