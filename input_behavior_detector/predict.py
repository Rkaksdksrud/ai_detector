import json
import pandas as pd
import joblib # 모델 저장을 위해 필요 (pip install joblib)
from src.features import get_combined_features

# 1. 학습된 모델 가져오기 (main.py에서 학습한 모델을 변수로 받거나 저장해서 써야 함)
# 테스트를 위해 main.py의 모델 학습 로직을 포함한 간단한 예측 함수를 만들겠습니다.

def predict_new_sample(model, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # 1개짜리 데이터프레임 생성
    df = pd.DataFrame([{
        'text': content.get('content', ''),
        'events': content.get('events', [])
    }])
    
    # 특징 추출
    features = get_combined_features(df)
    
    # 예측
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    
    label_map = {0: "Human (사람)", 1: "AI / Copy-Paste (복붙)"}
    
    print(f"\n[분석 결과]: {label_map[prediction]}")
    print(f"[확률]: 사람일 확률 {probability[0]*100:.2f}% / AI일 확률 {probability[1]*100:.2f}%")

# 이 코드를 실행하려면 main.py에서 학습된 model 객체가 필요합니다.