from huggingface_hub import snapshot_download

# 승인된 계정으로 로그인이 필요할 수 있습니다 (huggingface-cli login)
XDAC_path = "./XDAC_data"

snapshot_download(
    repo_id="keepsteady/XDAC_obs", 
    local_dir=XDAC_path,
    local_dir_use_symlinks=False
)