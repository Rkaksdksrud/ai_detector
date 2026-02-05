import json
import os
import sys
import requests

# 1. 엔진 로드를 위한 경로 설정
BASE_DIR = '/home/ktg0310/projects/ml_project/AI-dectector'
XDAC_DIR = os.path.join(BASE_DIR, 'XDAC_obs')
sys.path.append(BASE_DIR)
sys.path.append(XDAC_DIR)

def ask_ollama(content):
    url = "http://localhost:11434/api/generate"
    # 논문에서 언급된 '재구성(Rewrite)' 방식을 유도하는 프롬프트 [cite: 22, 35]
    prompt = f"다음 뉴스 댓글의 내용을 바탕으로 500자 이상의 논리적인 한국어 에세이를 작성해줘: '{content}'"
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 1000, "temperature": 0.7}
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        return response.json().get('response', '').strip()
    except:
        return None

try:
    # 암호화된 엔진 로드하여 실제 데이터 경로 추출
    from xdac_encrypted import AIUnifiedEngine, get_xdac_path
    actual_data_root = get_xdac_path()
    input_path = os.path.join(actual_data_root, 'LGC_data/LGC_data_v1.0.json')
    
    print(f"✅ 엔진이 찾은 실제 경로: {input_path}")

    with open(input_path, 'r', encoding='utf-8') as f:
        data_list = json.load(f)

    # 생성 로직 시작 (테스트를 위해 50건만)
    output_path = os.path.join(BASE_DIR, 'data/processed/ai_generated_essays.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    ai_essays = []
    print(f"🚀 Llama 3 에세이 생성 시작...")

    for i, item in enumerate(data_list[:50]):
        comment = item.get('generated_comment', '')
        if not comment: continue
        
        print(f"[{i+1}/50] 생성 중...", end=" ")
        essay = ask_ollama(comment)
        
        if essay and len(essay) >= 300:
            ai_essays.append({'text': essay, 'label': 1})
            print(f"성공! ({len(essay)}자)")
        else:
            print("실패 또는 길이 미달")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ai_essays, f, ensure_ascii=False, indent=4)
    print(f"✨ 저장 완료: {output_path}")

except Exception as e:
    print(f"❌ 실행 중 오류 발생: {e}")