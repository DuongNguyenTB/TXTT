from huggingface_hub import snapshot_download

# Ten model tieng Viet tren Hugging Face
model_name = "keepitreal/vietnamese-sbert"

# Thu muc dich luu model (Phai khop voi MODEL_PATH trong rag_logic.py)
save_path = "./models/vietnamese-sbert"

print(f"Bat dau tai model '{model_name}'...")
print("Qua trinh nay co the mat vai phut tuy toc do mang.")

# snapshot_download se keo toan bo file can thiet (gom ca config.json, modules.json...)
# giup Sentencetransformers load model offline thanh cong
snapshot_download(
    repo_id=model_name,
    local_dir=save_path,
    local_dir_use_symlinks=False
)

print(f"\n Da tai xong! Model duoc luu an toan tai: {save_path}")