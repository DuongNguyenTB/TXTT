Hướng dẫn cách thao tác trong phòng thi:
Bạn git clone toàn bộ source (bao gồm file main.py, client_exam.py và code RAG cá nhân của bạn) về máy.

Cài đặt các thư viện: pip install -r requirements.txt

Tải model Embedding về máy trước khi bị ngắt internet (trong 10-15p đầu).

Sửa lại các tham số MÃ_SINH_VIÊN_CỦA_BẠN và IP_MÁY_CỦA_BẠN cho đúng mạng LAN.

Mở terminal 1, chạy server của bạn: uvicorn main:app --host 0.0.0.0 --port 5000

Mở terminal 2, chạy file client_exam.py (chạy hàm register trước, sau đó là evaluate).

Phần việc quan trọng nhất bạn cần chuẩn bị ngay bây giờ là logic chunking và tích hợp một VectorDB chạy offline nhẹ nhàng (như ChromaDB hoặc FAISS với SentenceTransformers) vào thẳng Endpoint /upload và /ask nhé. Chúc bạn hoàn thiện code trơn tru!