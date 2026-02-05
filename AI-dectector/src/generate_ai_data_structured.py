import os
import json
import time
import google.generativeai as genai
from google.api_core import exceptions

# 1. Gemini 설정
MY_API_KEY = "AIzaSyAhXUOqGzWc4SV7BD4lVRKrn6AKCmyQsbk"
genai.configure(api_key=MY_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# 2. 경로 설정
SOURCE_BASE = "/home/ktg0310/ml_project/AI-dectector/data/human"
TARGET_BASE = "/home/ktg0310/ml_project/AI-dectector/data/ai"

def generate_with_retry(title, original_text, max_retries=5):
    """에러 발생 시 대기 후 재시도하는 함수"""
    prompt = f"뉴스 기자로서 다음 정보를 바탕으로 기사를 새로 작성하세요.\n제목: {title}\n내용: {original_text}"
    
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            return response.text.strip()
        except exceptions.ResourceExhausted as e:
            wait_time = (attempt + 1) * 10  # 10초, 20초... 점진적 대기
            print(f"🚨 할당량 초과! {wait_time}초 후 다시 시도합니다... ({e.message})")
            time.sleep(wait_time)
        except Exception as e:
            print(f"❌ 기타 에러 발생: {e}")
            break
    return None

count = 0

# 3. 데이터 생성 루프
for root, dirs, files in os.walk(SOURCE_BASE):
    json_files = [f for f in files if f.endswith('.json')]
    if not json_files: continue

    for file_name in json_files:
        source_file_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(root, SOURCE_BASE)
        target_dir = os.path.join(TARGET_BASE, relative_path)
        
        os.makedirs(target_dir, exist_ok=True)
        target_file_path = os.path.join(target_dir, file_name)

        # 이미 생성된 파일은 건너뛰기 (가장 중요!)
        if os.path.exists(target_file_path):
            continue

        try:
            with open(source_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            title = data.get('Meta(Acqusition)', {}).get('doc_name', '제목 없음')
            original_text = data.get('Meta(Refine)', {}).get('passage', '')

            if not original_text: continue

            print(f"📝 진행 중 [{count+1}]: {relative_path}/{file_name}")
            ai_text = generate_with_retry(title, original_text)
            
            if ai_text:
                data['Meta(Refine)']['passage'] = ai_text
                data['Meta(Refine)']['passage_id'] += "-AI"
                
                with open(target_file_path, 'w', encoding='utf-8') as out_f:
                    json.dump(data, out_f, ensure_ascii=False, indent=4)
                
                count += 1
                # 무료 티어 안정성을 위해 대기 시간 증가
                time.sleep(5) 

        except Exception as e:
            print(f"⚠ 파일 오류 ({file_name}): {e}")

print(f"✅ 작업 완료! 총 {count}개의 데이터가 생성되었습니다.")