# Hệ thống RAG Offline - PTIT Competition

Dự án xây dựng hệ thống cung cấp API Endpoint để truy vấn tài liệu sử dụng LLM + RAG với framework FastAPI, phục vụ cho kỳ thi cuối kỳ Offline RAG Competition trên mạng LAN.

##  Cấu trúc thư mục dự án

```text
├── models/
│   └── all-MiniLM-L6-v2/       # Thư mục lưu model embedding chạy offline (tải trước khi thi)
├── main.py                     # Server FastAPI chính của sinh viên (chứa endpoint /upload và /ask)
├── rag_logic.py                # Logic xử lý RAG (Chunking, Local FAISS VectorDB, Retrieval)
├── download_model.py           # Script tải model embedding từ Hugging Face về local (chạy khi có mạng)
├── client_exam.py              # Script gọi API điều phối của Teacher Server (register, evaluate, reset...)
└── requirements.txt            # Danh sách các thư viện cần cài đặt

 Hướng dẫn chuẩn bị và triển khai (Từng bước)
Bước 1: Cài đặt thư viện (Thực hiện khi CÓ mạng)
Mở terminal tại thư mục gốc của dự án và chạy lệnh sau để cài đặt toàn bộ các gói phụ thuộc:

pip install -r requirements.txt

Bước 2: Tải Model Embedding về Local (Thực hiện khi CÓ mạng)

Trước khi hệ thống ngắt kết nối internet, chạy script sau để kéo toàn bộ file vật lý của model về ổ cứng:

python download_model.py

Lưu ý: Kiểm tra xem thư mục models/all-MiniLM-L6-v2/ đã xuất hiện đầy đủ các file trọng số chưa trước khi báo giảng viên ngắt mạng.

Bước 3: Cấu hình thông tin phòng thi

Mở file main.py và client_exam.py.

Thay đổi giá trị biến STUDENT_ID thành Mã sinh viên của bạn (viết hoa).

Cập nhật TEACHER_SERVER_IP và STUDENT_SERVER_URL theo dải địa chỉ IP LAN thực tế được cấp tại phòng máy.

Bước 4: Khởi chạy Student Server (Môi trường OFFLINE)

Khi phòng thi ngắt mạng, bật server FastAPI của bạn lên để sẵn sàng nhận request từ hệ thống chấm điểm:

Bash
uvicorn main:app --host 0.0.0.0 --port 5000
Bước 5: Thao tác chấm điểm thi
Mở một terminal mới và sử dụng file client_exam.py để điều khiển luồng thi:

Mở hàm register() trong file client_exam.py và chạy để đăng ký IP máy của bạn với Teacher Server.

Comment hàm register() lại, mở hàm evaluate() ra và chạy để kích hoạt quá trình bắn tài liệu và 10 câu hỏi tự động.

Sử dụng các hàm bổ trợ như check_result() để xem tiến độ hoặc reset() để làm lại từ đầu nếu ứng dụng gặp sự cố.

Quy định đặc biệt về API Endpoint Sinh viên
Hệ thống chấm điểm tự động sẽ tương tác ngược lại với máy của bạn qua 2 cổng sau:

1. POST /upload
Chức năng: Nhận văn bản tài liệu gốc, thực hiện cắt nhỏ văn bản (Chunking) và nạp vào cơ sở dữ liệu vector (VectorDB) trên RAM.

Thời gian xử lý tối đa: 120 giây.

2. POST /ask
Chức năng: Nhận câu hỏi truy vấn trắc nghiệm, tìm kiếm ngữ cảnh phù hợp từ VectorDB, gửi prompt tới Proxy LLM để sinh kết quả.

Thời gian xử lý tối đa: 60 giây.

Yêu cầu kết quả: Thuộc tính answer trả về BẮT BUỘC chỉ được chứa đúng 1 ký tự duy nhất đại diện cho đáp án: A, B, C, hoặc D.