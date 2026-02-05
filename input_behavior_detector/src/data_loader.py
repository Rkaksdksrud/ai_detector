import os
import json
import pandas as pd

def load_dataset(base_path):
    data_list = []
    # 분류 목표: human(0), ai_or_copy(1)
    categories = {'human': 0, 'ai': 1} 

    for category, label in categories.items():
        folder_path = os.path.join(base_path, category)
        if not os.path.exists(folder_path):
            continue
            
        for file_name in os.listdir(folder_path):
            if file_name.endswith('.json'):
                file_path = os.path.join(folder_path, file_name)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    
                    # 분석에 필요한 핵심 정보 추출
                    data_list.append({
                        'text': content.get('content', ''),
                        'events': content.get('events', []),
                        'label': label,
                        'file_name': file_name
                    })
    
    return pd.DataFrame(data_list)

if __name__ == "__main__":
    # 경로 설정 (사용자 경로에 맞춰 수정 가능)
    BASE_DATA_PATH = "/home/ktg0310/projects/ml_project/input_behavior_detector/data/raw"
    df = load_dataset(BASE_DATA_PATH)
    print(f"로드 완료! 데이터 수: {len(df)}")
    print(df.head())