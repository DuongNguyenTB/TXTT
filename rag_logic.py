import argparse
import json
import os
from pathlib import Path
from typing import Any

import requests

# Cau hinh
TEACHER_SERVER_IP = os.getenv("TEACHER_SERVER_IP", "10.170.45.200").strip()
TEACHER_BASE_URL = os.getenv(
    "TEACHER_BASE_URL", f"http://{TEACHER_SERVER_IP}:8000/api/v1"
).strip()
STUDENT_ID = os.getenv("STUDENT_ID", "B21DCCN598").strip().upper()
STUDENT_SERVER_URL = os.getenv("STUDENT_SERVER_URL", "http://10.170.45.74:5000").strip()
REQUEST_TIMEOUT = float(os.getenv("CLIENT_TIMEOUT", "30"))

HEADERS = {"X-Student-ID": STUDENT_ID, "Content-Type": "application/json"}
STATE_FILE = Path(
    os.getenv("CLIENT_STATE_FILE", Path(__file__).resolve().parent / "exam_state.json")
)
MAX_SUBMISSIONS = int(os.getenv("MAX_SUBMISSIONS", "5"))

def _load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"document_received": False, "evaluate_calls": 0}
    try:
        data = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"document_received": False, "evaluate_calls": 0}
        return {
            "document_received": bool(data.get("document_received", False)),
            "evaluate_calls": int(data.get("evaluate_calls", 0)),
        }
    except Exception:
        return {"document_received": False, "evaluate_calls": 0}

def _save_state(state: dict[str, Any]) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def _reset_state() -> None:
    _save_state({"document_received": False, "evaluate_calls": 0})

def _print_response(response: requests.Response):
    print("STATUS:", response.status_code)
    try:
        print(response.json())
    except ValueError:
        print(response.text)

def _is_success(response: requests.Response) -> bool:
    payload = response.json() if response.status_code == 200 else {}
    status_text = str(payload.get("status", "")).lower()
    return status_text in {"ok", "success", "registered", "done"}

def register():
    print(">>> [POST] Dang ky Student Server...")
    url = f"{TEACHER_BASE_URL}/competition/register"
    res = requests.post(url, headers=HEADERS, json={"server_url": STUDENT_SERVER_URL}, timeout=REQUEST_TIMEOUT)
    _print_response(res)
    if _is_success(res):
        _reset_state()
        print({"trang_thai": "reset", "ly_do": "dang_ky_thanh_cong"})

def evaluate(document_received_override: bool | None = None):
    state = _load_state()
    if int(state.get("evaluate_calls", 0)) >= MAX_SUBMISSIONS:
        print({"canh_bao": "Da dat gioi han 5 lan nop!"})
    
    document_received = document_received_override if document_received_override is not None else state.get("document_received", False)
    payload = {"document_received": bool(document_received)}
    
    print(f">>> [POST] Bat dau evaluate (document_received={document_received})...")
    res = requests.post(f"{TEACHER_BASE_URL}/competition/evaluate", headers=HEADERS, json=payload, timeout=REQUEST_TIMEOUT)
    _print_response(res)
    
    if _is_success(res):
        state["document_received"] = True
    state["evaluate_calls"] = int(state.get("evaluate_calls", 0)) + 1
    _save_state(state)

def check_result():
    print(">>> [GET] Kiem tra ket qua...")
    res = requests.get(f"{TEACHER_BASE_URL}/competition/result", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    _print_response(res)

def reset():
    print(">>> [POST] Reset trang thai thi...")
    res = requests.post(f"{TEACHER_BASE_URL}/competition/reset", headers=HEADERS, timeout=REQUEST_TIMEOUT)
    _print_response(res)
    if _is_success(res):
        _reset_state()

if __name__ == "__main__":
    # Su dung: python client_exam.py [action]
    # actions: register, evaluate, result, reset, full
    # Vi du nop bai lan 1: python client_exam.py evaluate --document-received false
    # Vi du nop bai lan 2+: python client_exam.py evaluate --document-received true
    pass