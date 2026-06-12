import requests

# ==========================================
# CAU HINH HE THONG (Thay doi khi vao phong thi)
# ==========================================
# Bat buoc phai co /v1 o cuoi duong dan cua Teacher Server
TEACHER_BASE_URL = "http://192.168.50.218:8000/api/v1" 
STUDENT_ID = "B21DCCNxxx" # Ma sinh vien viet hoa cua ban
STUDENT_SERVER_URL = "http://192.168.1.15:5000" # IP mang LAN may cua ban

HEADERS = {
    "X-Student-ID": STUDENT_ID,
    "Content-Type": "application/json"
}

def register():
    """1. Dang ky dia chi Student Server voi Teacher Server"""
    print("\n>>> [POST] Dang dang ky voi Teacher Server...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/register",
            headers=HEADERS,
            json={"server_url": STUDENT_SERVER_URL}
        )
        data = res.json()
        print(f"Loi nhan: {data.get('message')}")
        print(f"Sinh vien: {data.get('student_id')} | Server: {data.get('server_url')}")
    except Exception as e:
        print(f"Loi ket noi: {e}")

def evaluate(document_received=False):
    """2. Kich hoat qua trinh cham diem tu dong"""
    print(f"\n>>> [POST] Bat dau thi (document_received={document_received})...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/evaluate",
            headers=HEADERS,
            json={"document_received": document_received}
        )
        data = res.json()
        print(f"Trang thai: {data.get('message')}")
        print(f"Diem so cuoi cung: {data.get('final_score')}")
    except Exception as e:
        print(f"Loi ket noi: {e}")

def check_result():
    """3. Kiem tra tien do cau hoi va diem so hien tai khi dang thi"""
    print("\n>>> [GET] Kiem tra trang thai hien tai...")
    try:
        res = requests.get(
            f"{TEACHER_BASE_URL}/competition/result",
            headers=HEADERS
        )
        data = res.json()
        print(f"Sinh vien: {data.get('student_id')}")
        print(f"Trang thai he thong: {data.get('status')}")
        print(f"Dang o cau hoi so: {data.get('current_question')}/100") 
        print(f"Diem so hien tai: {data.get('score')}")
    except Exception as e:
        print(f"Loi ket noi: {e}")

def reset():
    """4. Reset trang thai thi ve ban dau neu code gap su co giua chung"""
    print("\n>>> [POST] Yeu cau reset trang thai thi...")
    try:
        res = requests.post(
            f"{TEACHER_BASE_URL}/competition/reset",
            headers=HEADERS
        )
        data = res.json()
        print(f"Trang thai: {data.get('status')}")
        print(f"Loi nhan: {data.get('message')}")
        print(f"Diem so luu lai truoc do: {data.get('score')}")
    except Exception as e:
        print(f"Loi ket noi: {e}")

# ==========================================
# KHU VUC CHAY THUC TE
# ==========================================
if __name__ == "__main__":
    # Buoc 1: Dang ky IP may minh voi giang vien
    register()
    
    # Buoc 2: Nop bai (Chi duoc nop toi da 5 lan)
    
    # --- Lan nop DAU TIEN (De may chu gui tai lieu ve cho ban embed) ---
    # evaluate(document_received=False) 
    
    # --- Lan nop THU 2, 3, 4, 5 (Da luu VectorDB local, khong can cho gui lai tai lieu) ---
    # evaluate(document_received=True)
    
    # Cac ham bo tro (Bo comment de dung khi can):
    # check_result()
    # reset()