import os
import json

target_file = '/home/ktg0310/ml_project/AI-dectector/XDAC_obs/xdac_encrypted.py'
output_path = '/home/ktg0310/ml_project/AI-dectector/data/processed/ai_essays_300.json'

print("🏗️ 엔진 로드 없이 파일에서 데이터만 강제 추출 시작...")

try:
    # 1.1GB 파일을 한 번에 decode하면 메모리 에러가 날 수 있으므로 rb로 읽습니다.
    with open(target_file, 'rb') as f:
        content = f.read()

    # 데이터셋의 시작 패턴을 찾습니다. 
    # XDAC 데이터는 보통 [{"passage": 로 시작하는 JSON 리스트입니다.
    start_pattern = b'[{"passage":'
    start_idx = content.find(start_pattern)

    if start_idx == -1:
        print("❌ 데이터 시작 패턴을 찾지 못했습니다. 다른 패턴으로 시도합니다...")
        # 대안 패턴: AI 모델명 등이 포함된 구간 검색
        start_pattern = b'[{"model":'
        start_idx = content.find(start_pattern)

    if start_idx != -1:
        # 끝 패턴 (리스트의 끝)을 찾습니다.
        end_idx = content.rfind(b'}]') + 2
        json_bytes = content[start_idx:end_idx]
        
        print(f"✅ 데이터 구간 발견 (크기: {len(json_bytes)/1024/1024:.2f} MB)")
        
        # JSON 파싱
        data_list = json.loads(json_bytes.decode('utf-8', errors='ignore'))
        print(f"✅ {len(data_list):,}건의 원본 데이터 확보!")

        # 300자 이상 필터링 (에세이 기준)
        min_length = 300
        long_essays = [
            {
                'text': item.get('passage', ''),
                'label': 1,
                'model': item.get('model', 'unknown')
            } 
            for item in data_list if len(item.get('passage', '')) >= min_length
        ]
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(long_essays, f, ensure_ascii=False, indent=4)

        print(f"📊 최종 결과: {len(long_essays):,}건의 AI 에세이 추출 성공")
        print(f"📍 저장 위치: {output_path}")
    else:
        print("❌ 파일 내부에서 JSON 데이터 구조를 찾을 수 없습니다.")

except Exception as e:
    print(f"❌ 추출 중 오류 발생: {e}")