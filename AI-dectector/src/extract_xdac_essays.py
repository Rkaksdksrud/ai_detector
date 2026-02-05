import os
import sys
import json
from unittest.mock import patch

# 1. 경로 설정
PROJECT_ROOT = '/home/ktg0310/ml_project/AI-dectector'
XDAC_DIR = os.path.join(PROJECT_ROOT, 'XDAC_obs')
ABS_MODEL_PATH = os.path.join(XDAC_DIR, 'XDAC-D')

# 파이썬 탐색 경로 추가 및 작업 디렉토리 변경
sys.path.append(XDAC_DIR)
os.chdir(XDAC_DIR)

def run_extraction():
    try:
        # 2. 엔진이 내부에서 호출하는 'AutoModel' 또는 'from_pretrained'의 경로를 강탈합니다.
        # Hugging Face가 ./ 로 시작하는 경로를 무시하도록 절대 경로로 덮어씌웁니다.
        import transformers
        
        original_from_pretrained = transformers.PreTrainedModel.from_pretrained
        
        @classmethod
        def patched_from_pretrained(cls, pretrained_model_name_or_path, *model_args, **kwargs):
            if pretrained_model_name_or_path == "./XDAC-D":
                pretrained_model_name_or_path = ABS_MODEL_PATH
            return original_from_pretrained(pretrained_model_name_or_path, *model_args, **kwargs)

        # 메서드 패치 적용
        with patch('transformers.PretrainedConfig.from_pretrained') as mock_conf:
            # config 로드 시 경로 치환을 위해 transformers 내부 동작을 가로챕니다.
            from xdac_encrypted import AIUnifiedEngine
            
            print("🔓 System Patched. Loading secure XDAC...")
            # 수동으로 transformers의 메서드를 덮어씌워 강제 로드 유도
            transformers.modeling_utils.PreTrainedModel.from_pretrained = patched_from_pretrained
            transformers.configuration_utils.PretrainedConfig.from_pretrained = patched_from_pretrained
            
            engine = AIUnifiedEngine() 
        
        print("✅ 엔진 및 데이터셋 로드 완료!")

        # 3. 데이터 추출 (300자 이상 에세이)
        print("🔍 에세이 필터링 중...")
        raw_data = engine.get_all_data() if hasattr(engine, 'get_all_data') else engine.dataset

        ai_essays = []
        for item in raw_data:
            text = item.get('passage', '')
            if len(text) >= 300:
                ai_essays.append({
                    'text': text,
                    'label': 1,
                    'model': item.get('model', 'unknown')
                })

        # 4. 결과 저장
        OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data/processed/ai_essays_300.json')
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(ai_essays, f, ensure_ascii=False, indent=4)

        print(f"📊 최종 결과: {len(ai_essays):,}건의 AI 에세이 확보")
        print(f"📍 저장 위치: {OUTPUT_FILE}")

    except Exception as e:
        print(f"❌ 최종 패치 실패: {e}")
        print("💡 마지막 수단: 'vi XDAC_obs/xdac_encrypted.py'에서 './XDAC-D'를 절대경로로 직접 바꾸세요.")

if __name__ == "__main__":
    run_extraction()