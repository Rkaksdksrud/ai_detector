import openai  # 혹은 활용하시는 다른 LLM API
import json
import time

# 1. 주제 리스트 (질문자님의 인간 에세이 주제들을 여기 넣으세요)
topics = ["인공지능의 윤리적 문제", "기후 변화와 개인의 역할", "현대 사회의 고독 문제"]

def generate_essay(topic):
    prompt = f"다음 주제에 대해 800자 내외의 한국어 에세이를 작성해줘: '{topic}'. 서론-본론-결론 구조를 갖추고 자연스럽게 써줘."
    
    # 예시: OpenAI API 사용 (질문자님의 환경에 맞게 수정 가능)
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# 2. 대량 생성 루프
ai_essays = []
for topic in topics:
    print(f"✍️ 주제 '{topic}'에 대한 AI 에세이 생성 중...")
    essay_text = generate_essay(topic)
    ai_essays.append({
        "text": essay_text,
        "label": 1,  # AI
        "topic": topic
    })
    time.sleep(1) # API 레이트 리밋 방지

# 3. 저장
with open('../processed/synthetic_ai_essays.json', 'w', encoding='utf-8') as f:
    json.dump(ai_essays, f, ensure_ascii=False, indent=4)