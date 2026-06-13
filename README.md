##  Cấu hình Biến môi trường (.env)

Hệ thống sử dụng các biến môi trường để dễ dàng thay đổi cấu hình mà không cần can thiệp trực tiếp vào mã nguồn. 

### Bước 1: Tạo file cấu hình
Tại thư mục gốc của dự án (cùng cấp với file `main.py`), hãy tạo một file mới có tên chính xác là `.env`.

### Bước 2: Khai báo các thông số
Copy toàn bộ nội dung dưới đây và dán vào file `.env` vừa tạo. Hãy thay đổi các giá trị `STUDENT_ID`, `TEACHER_SERVER_IP`, và `STUDENT_SERVER_URL` cho khớp với mạng LAN phòng thi của bạn:

```env
# ==========================================
# THÔNG TIN SINH VIÊN VÀ MẠNG LAN
# ==========================================
STUDENT_ID=B21DCCNxxx
TEACHER_SERVER_IP=192.168.50.218
STUDENT_SERVER_URL=[http://192.168.1.15:5000](http://192.168.1.15:5000)

# ==========================================
# CẤU HÌNH LLM (PROXY)
# ==========================================
# Tên model LLM do Teacher Server cung cấp (VD: gpt-4o-mini hoặc Qwen/...)
LLM_MODEL=gpt-4o-mini

# ==========================================
# CẤU HÌNH RAG & VECTOR DB
# ==========================================
EMBEDDING_MODEL_PATH=./models/vietnamese-sbert-base
FAISS_INDEX_DIR=./faiss_index
RAG_CHUNK_SIZE=500
RAG_CHUNK_OVERLAP=50
RETRIEVAL_TOP_K=3
MAX_CONTEXT_CHARS=4500

# ==========================================
# CẤU HÌNH CLIENT THI CỬ (client_exam.py)
# ==========================================
MAX_SUBMISSIONS=5
CLIENT_TIMEOUT=45.0


./models/all-MiniLM-L6-v2

# Hệ thống RAG Offline - PTIT Final Competition

Hệ thống cung cấp API Endpoint để truy vấn tài liệu sử dụng LLM + RAG với framework FastAPI, được tối ưu hóa bằng `faiss` thuần và `sentence-transformers` để đạt tốc độ cao nhất trong kỳ thi cuối kỳ Offline RAG.

## 📁 Cấu trúc thư mục dự án

```text
├── models/
│   └── vietnamese-sbert/       # Model embedding tiếng Việt chạy offline (tải trước khi thi)
├── faiss_index/                # Thư mục chứa Vector DB được tự động lưu xuống ổ cứng
├── main.py                     # Server FastAPI chính của sinh viên (chứa endpoint /upload và /ask)
├── rag_logic.py                # Logic RAG lõi (Chunking, Pure FAISS, Sentence-Transformers)
├── download_model.py           # Script tải model từ Hugging Face (dùng snapshot_download)
├── client_exam.py              # Script CLI điều phối tự động gọi API Teacher Server
├── exam_state.json             # File tự sinh để theo dõi số lần nộp bài (tối đa 5 lần)
└── requirements.txt            # Danh sách thư viện rút gọn tối ưu

Hướng dẫn Chuẩn bị (Khi CÓ mạng internet)
1. Cài đặt thư viện
Mở terminal và chạy lệnh:


pip install -r requirements.txt

2. Tải Model Embedding Tiếng Việt

Chạy script để kéo toàn bộ file vật lý của model keepitreal/vietnamese-sbert về ổ cứng:

python download_model.py

(Đảm bảo thư mục models/vietnamese-sbert/ đã có đầy đủ file trước khi báo giảng viên ngắt mạng)

Hướng dẫn Đi thi (Khi NGẮT mạng internet)
Bước 1: Cấu hình thông tin (Nếu cần)

Mở main.py và client_exam.py. Cập nhật STUDENT_ID và STUDENT_SERVER_URL (IP máy bạn) cho chuẩn xác với mạng LAN phòng thi.

Bước 2: Khởi chạy Student Server

Mở terminal số 1, chạy server FastAPI:

uvicorn main:app --host 0.0.0.0 --port 5000

Bước 3: Thao tác nộp bài bằng CLI Tool (client_exam.py)
Mở terminal số 2, dùng công cụ dòng lệnh đã được thiết kế sẵn để thi:

Đăng ký IP với máy chủ:

python client_exam.py register

Bắt đầu thi (Chấm điểm):


python client_exam.py evaluate

(Lưu ý: Hệ thống có cơ chế tự động ghi nhớ trạng thái vào file exam_state.json. Ở lần gọi đầu tiên, nó sẽ yêu cầu Teacher gửi tài liệu. Từ lần thứ 2 trở đi, nó sẽ tự động skip bước nhận tài liệu để tiết kiệm thời gian).

Các lệnh hỗ trợ khác:

Kiểm tra tiến độ / điểm số hiện tại: python client_exam.py result

Reset bài thi (nếu lỗi): python client_exam.py reset

Chạy tự động từ A-Z (Đăng ký + Nộp bài): python client_exam.py full

 Cảnh báo quan trọng
Giới hạn nộp bài: Chỉ được gọi lệnh evaluate tối đa 5 lần. Hệ thống script sẽ tự động cảnh báo nếu bạn nộp quá giới hạn này.

Số lượng câu hỏi: 100 câu hỏi. Thời gian chờ tối đa cho mỗi câu là 60s.

Nếu bạn tắt server main.py để sửa logic, khi bật lại, hệ thống sẽ tự động nạp lại dữ liệu từ faiss_index mà không cần embed lại từ đầu!