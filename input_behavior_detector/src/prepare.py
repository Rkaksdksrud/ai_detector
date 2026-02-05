from sklearn.model_selection import train_test_split
from src.data_loader import load_dataset

def prepare_data():
    BASE_PATH = "/home/ktg0310/projects/ml_project/input_behavior_detector/data/raw"
    df = load_dataset(BASE_PATH)
    
    # 텍스트와 라벨 분리
    # (지금은 우선 텍스트와 이벤트 로그 전체를 넘기고, 나중에 features.py에서 가공합니다)
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df['label'])
    
    print(f"학습 데이터: {len(train_df)}개")
    print(f"테스트 데이터: {len(test_df)}개")
    
    return train_df, test_df

if __name__ == "__main__":
    prepare_data()