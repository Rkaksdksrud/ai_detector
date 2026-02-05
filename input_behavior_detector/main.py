import pandas as pd
from src.prepare import prepare_data
from src.features import get_combined_features
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

def run_experiment():
    # 1. 데이터 로드 및 분할
    print("--- 데이터 로딩 중 ---")
    train_df, test_df = prepare_data()
    
    # 2. 특징 추출 (Feature Extraction)
    print("--- 특징 추출 중 ---")
    X_train = get_combined_features(train_df)
    y_train = train_df['label']
    
    X_test = get_combined_features(test_df)
    y_test = test_df['label']
    
    # 3. 모델 학습 (Random Forest)
    print("--- 모델 학습 시작 ---")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # 4. 성능 평가
    print("--- 성능 평가 결과 ---")
    y_pred = model.predict(X_test)
    
    # 리포트 출력
    print(classification_report(y_test, y_pred, target_names=['Human', 'AI/Copy']))
    
    # 5. 특징 중요도 확인 (어떤 단서가 가장 유용했나?)
    importances = model.feature_importances_
    feature_names = X_train.columns
    feature_importance_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
    print("\n[특징 중요도]")
    print(feature_importance_df.sort_values(by='importance', ascending=False))

if __name__ == "__main__":
    run_experiment()