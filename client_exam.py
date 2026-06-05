import requests

# Cấu hình
TEACHER_BASE_URL = "http://192.168.50.218:8000/api/v1"
STUDENT_ID = "MÃ_SINH_VIÊN_CỦA_BẠN" # Yêu cầu viết hoa
STUDENT_SERVER_URL = "http://<IP_MÁY_CỦA_BẠN>:5000" # Nhớ thay bằng IP LAN thực tế của máy bạn

HEADERS = {
    "X-Student-ID": STUDENT_ID,
    "Content-Type": "application/json"
}

def register():
    print(">>> Đang đăng ký với Teacher Server...")
    res = requests.post(
        f"{TEACHER_BASE_URL}/competition/register",
        headers=HEADERS,
        json={"server_url": STUDENT_SERVER_URL}
    )
    print(res.json())

def evaluate():
    print(">>> Bắt đầu quá trình thi (Evaluate)...")
    res = requests.post(
        f"{TEACHER_BASE_URL}/competition/evaluate",
        headers=HEADERS
    )
    print(res.json())

def check_result():
    print(">>> Kiểm tra kết quả...")
    res = requests.get(
        f"{TEACHER_BASE_URL}/competition/result",
        headers=HEADERS
    )
    print(res.json())

def reset():
    print(">>> Reset trạng thái thi...")
    res = requests.post(
        f"{TEACHER_BASE_URL}/competition/reset",
        headers=HEADERS
    )
    print(res.json())

if __name__ == "__main__":
    # Bỏ comment hàm bạn muốn chạy
    
    # BƯỚC 1: Gọi register 1 lần
    register()
    
    # BƯỚC 2: Gọi evaluate để Teacher Server bắt đầu bắn request vào /upload và /ask
    # evaluate()
    
    # KHI CẦN:
    # check_result()
    # reset()