import requests

# ==========================================
# CẤU HÌNH HỆ THỐNG (Thay đổi khi vào phòng thi)
# ==========================================
# Bắt buộc phải có /v1 ở cuối đường dẫn của Teacher Server
TEACHER_BASE_URL = "http://192.168.50.218:8000/api/v1" 
STUDENT_ID = "B21DCCNxxx" # Mã sinh viên viết hoa của bạn
STUDENT_SERVER_URL = "http://192.168.1.15:5000" # IP mạng LAN máy của bạn

HEADERS = {
    "X-Student-ID": STUDENT_ID,
    "Content-Type": "application/json"
}

def register():
    """1. Đăng ký địa chỉ Student Server với Teacher Server"""
    print("\n>>> [POST] Đang đăng ký với Teacher Server...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/register",
            headers=HEADERS,
            json={"server_url": STUDENT_SERVER_URL}
        )
        data = res.json()
        print(f"Lời nhắn: {data.get('message')}")
        print(f"Sinh viên: {data.get('student_id')} | Server: {data.get('server_url')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

def evaluate(document_received=False):
    """2. Kích hoạt quá trình chấm điểm tự động"""
    print(f"\n>>> [POST] Bắt đầu thi (document_received={document_received})...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/evaluate",
            headers=HEADERS,
            json={"document_received": document_received}
        )
        data = res.json()
        print(f"Trạng thái: {data.get('message')}")
        print(f"Điểm số cuối cùng: {data.get('final_score')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

def check_result():
    """3. Kiểm tra tiến độ câu hỏi và điểm số hiện tại khi đang thi"""
    print("\n>>> [GET] Kiểm tra trạng thái hiện tại...")
    try:
        res = requests.get(
            f"{TEACHER_BASE_URL}/competition/result",
            headers=HEADERS
        )
        data = res.json()
        print(f"Sinh viên: {data.get('student_id')}")
        print(f"Trạng thái hệ thống: {data.get('status')}")
        print(f"Đang ở câu hỏi số: {data.get('current_question')}/100") # <-- Đã sửa thành 100
        print(f"Điểm số hiện tại: {data.get('score')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

def reset():
    """4. Reset trạng thái thi về ban đầu nếu code gặp sự cố giữa chừng"""
    print("\n>>> [POST] Yêu cầu reset trạng thái thi...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/reset",
            headers=HEADERS
        )
        data = res.json()
        print(f"Trạng thái: {data.get('status')}")
        print(f"Lời nhắn: {data.get('message')}")
        print(f"Điểm số lưu lại trước đó: {data.get('score')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

# ==========================================
# KHU VỰC CHẠY THỰC TẾ
# ==========================================
if __name__ == "__main__":
    # Bước 1: Đăng ký IP máy mình với giảng viên
    register()
    
    # Bước 2: Nộp bài (Chỉ được nộp tối đa 5 lần)
    
    # --- Lần nộp ĐẦU TIÊN (Để máy chủ gửi tài liệu về cho bạn embed) ---
    # evaluate(document_received=False) 
    
    # --- Lần nộp THỨ 2, 3, 4, 5 (Đã lưu VectorDB local, không cần chờ gửi lại tài liệu) ---
    # evaluate(document_received=True)
    
    # Các hàm bổ trợ (Bỏ comment để dùng khi cần):
    # check_result()
    # reset()