import os
from huggingface_hub import snapshot_download

# 1. 모델 및 데이터 다운로드 (승인된 계정으로 로그인 상태여야 함)
XDAC_root_path = '/home/ktg0310/ml_project/AI-dectector/XDAC_obs'
snapshot_download(
    repo_id="keepsteady/XDAC_obs",
    local_dir=XDAC_root_path,
    local_dir_use_symlinks=False
)

# 2. 데이터 로드 확인
import json
path_data = os.path.join(XDAC_root_path, 'LGC_data/LGC_data_v1.0.json')
with open(path_data, 'r', encoding='utf-8') as f:
    lgc_data = json.load(f)

print(f"✅ AI 데이터 {len(lgc_data)}건 로드 완료!")