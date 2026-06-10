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
        # Slide mới trả về 'message' thay vì 'status'
        print(f"Lời nhắn: {data.get('message')}")
        print(f"Sinh viên: {data.get('student_id')} | Server: {data.get('server_url')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

def evaluate():
    """2. Kích hoạt quá trình chấm điểm tự động (Bắn tài liệu + 10 câu hỏi)"""
    print("\n>>> [POST] Bắt đầu quá trình thi (Evaluate)...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/evaluate",
            headers=HEADERS
        )
        data = res.json()
        # Slide mới trả về 'message' và 'final_score'
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
        print(f"Đang ở câu hỏi số: {data.get('current_question')}/10")
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
        # Slide mới bổ sung thêm trường 'score' ở hàm reset
        print(f"Trạng thái: {data.get('status')}")
        print(f"Lời nhắn: {data.get('message')}")
        print(f"Điểm số lưu lại trước đó: {data.get('score')}")
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

if __name__ == "__main__":
    # Trong phòng thi, bạn cần chạy hàm nào thì bỏ dấu thăng (#) ở hàm đó ra nhé
    
    # Bước đầu tiên: Đăng ký IP máy mình với giảng viên
    register()
    
    # Bước hai: Kích hoạt chấm điểm
    # evaluate()
    
    # Các hàm bổ trợ dùng khi cần thiết:
    # check_result()
    # reset()