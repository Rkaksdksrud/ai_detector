# human 데이터의 요약 내용을 바탕으로 한국어 에세이 작성 프로그램 -> AI 데이터로 활용


import json
import os
import glob
import requests

# 1. 경로 설정
BASE_DIR = '/home/ktg0310/projects/ml_project/AI-dectector'
# '라벨링데이터' 폴더까지만 지정하면 하위 01~10 폴더를 모두 뒤집니다.
HUMAN_ROOT = os.path.join(BASE_DIR, 'data/human/1.Training/라벨링데이터/TL1')
OUTPUT_PATH = os.path.join(BASE_DIR, 'data/processed/combined_ai_human_data.json')

def ask_llama3(summary_text):
    """로컬 Ollama(Llama3)를 사용하여 요약문을 긴 에세이로 확장합니다."""
    url = "http://localhost:11434/api/generate"
    prompt = f"""
    당신은 전문 작가입니다. 다음 '요약 내용'을 바탕으로 약 800자 내외의 한국어 에세이를 작성하세요.
    
    [요약 내용]: {summary_text}
    
    [작성 가이드]:
    1. 논리적인 서론-본론-결론 구조를 갖출 것.
    2. 전문적이고 분석적인 문체를 사용할 것.
    3. 한국어로만 작성할 것.
    
    에세이 시작:
    """
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False,
        "options": {"num_predict": 1500, "temperature": 0.7}
    }
    try:
        response = requests.post(url, json=payload, timeout=120)
        return response.json().get('response', '').strip()
    except:
        return None

# 2. 메인 실행 로직
def main():
    # 모든 하위 폴더의 JSON 파일 리스트 확보
    json_files = glob.glob(os.path.join(HUMAN_ROOT, '**/*.json'), recursive=True)
    print(f"🔍 총 {len(json_files)}개의 파일을 발견했습니다.")

    dataset = []
    # 테스트를 위해 우선 100개만 진행 (성공 시 [:100] 제거)
    for i, file_path in enumerate(json_files[:100]):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 1) 인간 데이터 추출 (passage)
            passage = data.get('Meta(Refine)', {}).get('passage', '')
            
            # 2) AI 에세이 생성을 위한 요약문 추출 (summary1)
            summary = data.get('Annotation', {}).get('summary1', '')

            if len(passage) >= 300 and summary:
                print(f"[{i+1}/100] 에세이 생성 중... ({os.path.basename(file_path)})")
                
                # Llama3로 AI 데이터 생성
                ai_essay = ask_llama3(summary)
                
                if ai_essay and len(ai_essay) >= 300:
                    # 인간 데이터 저장 (Label 0)
                    dataset.append({'text': passage, 'label': 0, 'source': 'human'})
                    # 생성된 AI 데이터 저장 (Label 1)
                    dataset.append({'text': ai_essay, 'label': 1, 'source': 'llama3'})
                    print(f"   ✅ 완료 (인간: {len(passage)}자 / AI: {len(ai_essay)}자)")
                
        except Exception as e:
            print(f"   ❌ 오류 발생 ({file_path}): {e}")

        # 10건마다 중간 저장
        if (i + 1) % 10 == 0:
            with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
                json.dump(dataset, f, ensure_ascii=False, indent=4)

    print(f"✨ 작업 완료! 총 {len(dataset)}건의 데이터가 {OUTPUT_PATH}에 저장되었습니다.")

if __name__ == "__main__":
    main()