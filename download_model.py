from huggingface_hub import snapshot_download

# Tên model tiếng Việt bạn vừa tìm được
model_name = "keepitreal/vietnamese-sbert"

# Sửa lại tên thư mục lưu cho khớp
save_path = "./models/vietnamese-sbert"

print(f"Bắt đầu tải model '{model_name}'...")
snapshot_download(
    repo_id=model_name,
    local_dir=save_path,
    local_dir_use_symlinks=False
)

print(f"\n Đã tải xong! Model được lưu tại: {save_path}")