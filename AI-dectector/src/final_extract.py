import os
import sys
import json

# 1. 절대 경로 설정 (이 부분이 가장 중요합니다)
# xdac_encrypted.py 파일이 들어있는 '폴더'의 상위 경로를 지정해야 합니다.
BASE_DIR = '/home/ktg0310/ml_project/AI-dectector'
XDAC_DIR = os.path.join(BASE_DIR, 'XDAC_obs')

# 파이썬 탐색 경로에 추가
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if XDAC_DIR not in sys.path:
    sys.path.append(XDAC_DIR)

# 2. 엔진 모듈 로드
try:
    # 폴더 구조에 따라 두 가지 방식 중 하나로 로드됩니다.
    try:
        from XDAC_obs.xdac_encrypted import AIUnifiedEngine, get_xdac_path
    except ImportError:
        from xdac_encrypted import AIUnifiedEngine, get_xdac_path
    
    print("🔓 Loading secure XDAC...")
    # 엔진이 인식하는 실제 데이터 루트 경로를 가져옵니다.
    XDAC_root_path = get_xdac_path()
    print(f"✅ Secure XDAC imported! Path: {XDAC_root_path}")

    # 3. 데이터 로드 및 300자 이상 필터링
    # 예제 코드의 경로 규칙을 그대로 따릅니다.
    path_data = os.path.join(XDAC_root_path, 'LGC_data', 'LGC_data_v1.0.json')
    
    print("🔍 1.1GB 대규모 데이터 분석 시작...")
    with open(path_data, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    min_len = 300
    ai_essays = []

    for item in data_list:
        passage = item.get('passage', '')
        if len(passage) >= min_len:
            ai_essays.append({
                'text': passage,
                'label': 1, # AI 레이블
                'model': item.get('model', 'unknown')
            })

    # 4. 필터링된 결과 저장
    output_dir = '/home/ktg0310/ml_project/AI-dectector/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'ai_essays_300.json')

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ai_essays, f, ensure_ascii=False, indent=4)

    print("-" * 50)
    print(f"📊 추출 결과")
    print(f"- 원본 데이터: {len(data_list):,}건")
    print(f"- 300자 이상 에세이: {len(ai_essays):,}건")
    print(f"- 저장 경로: {output_path}")
    print("-" * 50)

except Exception as e:
    print(f"❌ 오류 발생: {e}")