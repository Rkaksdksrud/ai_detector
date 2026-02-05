import os
import sys
import json

BASE_DIR = '/home/ktg0310/ml_project/AI-dectector'
XDAC_DIR = os.path.join(BASE_DIR, 'XDAC_obs')
sys.path.append(BASE_DIR)
sys.path.append(XDAC_DIR)

try:
    from xdac_encrypted import AIUnifiedEngine, get_xdac_path
    
    print("🔓 Loading XDAC Engine...")
    actual_path = get_xdac_path()
    path_data = os.path.join(actual_path, 'LGC_data/LGC_data_v1.0.json')
    
    with open(path_data, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    print(f"✅ 데이터 로드 완료: {len(data_list):,}건")
    
    # 실제 텍스트가 담긴 필드: 'generated_comment'
    field_name = 'generated_comment'
    
    # 길이 분석
    lengths = []
    for item in data_list:
        text = item.get(field_name, "")
        if text is None: text = ""
        lengths.append(len(str(text)))
    
    lengths.sort(reverse=True)

    print("-" * 50)
    print(f"📊 '{field_name}' 필드 길이 분포")
    print(f"- 최대 길이: {lengths[0]}자")
    print(f"- 상위 10개 평균: {sum(lengths[:10])//10}자")
    print(f"- 200자 이상 데이터 개수: {len([l for l in lengths if l >= 200])}건")
    print("-" * 50)

    # 300자 이상 추출 시도 (댓글 데이터라 수량이 적을 수 있음)
    min_len = 300
    ai_essays = []
    for item in data_list:
        text = str(item.get(field_name, ""))
        if len(text) >= min_len:
            ai_essays.append({
                'text': text,
                'label': 1,
                'model': item.get('llm_model_selection', 'unknown'),
                'sentiment': item.get('sentiment', 'unknown')
            })

    if not ai_essays:
        print(f"⚠️ {min_len}자 이상이 0건입니다. 데이터셋이 단문 위주인 것 같습니다.")
    else:
        output_path = os.path.join(BASE_DIR, 'data/processed/ai_comments_long.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ai_essays, f, ensure_ascii=False, indent=4)
        print(f"💾 {len(ai_essays)}건 저장 완료: {output_path}")

except Exception as e:
    print(f"❌ 오류 발생: {e}")