import numpy as np
import pandas as pd

def extract_behavior_features(events):
    """
    이벤트 로그에서 행동 특징(타이핑 리듬, 복붙 여부 등)을 추출합니다.
    """
    if not events:
        return pd.Series({
            'avg_iki': 0, 'std_iki': 0, 'paste_count': 0, 
            'delete_count': 0, 'total_events': 0
        })

    # 1. 키 입력 간격 (Inter-Key Interval, IKI) 추출
    key_times = [e['time'] for e in events if e['type'] == 'keydown']
    ikis = np.diff(key_times) if len(key_times) > 1 else [0]
    
    # 2. 복사 붙여넣기 횟수 및 총 글자수
    paste_events = [e for e in events if e['type'] == 'paste']
    paste_count = len(paste_events)
    
    # 3. 삭제/수정 횟수 (Backspace, Delete)
    delete_count = len([e for e in events if e.get('key') in ['Backspace', 'Delete']])

    return pd.Series({
        'avg_iki': np.mean(ikis) if len(ikis) > 0 else 0,   # 평균 입력 간격
        'std_iki': np.std(ikis) if len(ikis) > 0 else 0,    # 입력 리듬의 불규칙성
        'paste_count': paste_count,                         # 복붙 횟수
        'delete_count': delete_count,                       # 수정 횟수
        'total_events': len(events)                         # 전체 이벤트 수
    })

def extract_text_features(text):
    """
    텍스트 자체의 구조적 특징(문장 길이, 단어 다양성 등)을 추출합니다.
    """
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    
    # 단어 다양성 (Unique Words / Total Words)
    unique_ratio = len(set(words)) / word_count if word_count > 0 else 0
    
    return pd.Series({
        'word_count': word_count,
        'char_count': char_count,
        'unique_word_ratio': unique_ratio
    })

def get_combined_features(df):
    """
    행동 특징과 텍스트 특징을 합쳐서 하나의 학습용 데이터프레임을 만듭니다.
    """
    behavior_df = df['events'].apply(extract_behavior_features)
    text_df = df['text'].apply(extract_text_features)
    
    return pd.concat([behavior_df, text_df], axis=1)