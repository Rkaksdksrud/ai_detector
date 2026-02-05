import os

# 1. 경로 설정
target_file = '/home/ktg0310/ml_project/AI-dectector/XDAC_obs/xdac_encrypted.py'
old_path = "./XDAC-D"
new_path = "/home/ktg0310/ml_project/AI-dectector/XDAC_obs/XDAC-D"

if not os.path.exists(target_file):
    print(f"❌ 파일을 찾을 수 없습니다: {target_file}")
    exit()

print(f"🛠️ 엔진 코드 패치 시작 (대용량 파일이므로 시간이 걸릴 수 있습니다)...")

try:
    # 파일을 읽어서 특정 문자열만 치환
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if old_path in content:
        new_content = content.replace(old_path, new_path)
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ 패치 완료: '{old_path}' -> '{new_path}'")
    else:
        print("ℹ️ 이미 패치되었거나 해당 문자열을 찾을 수 없습니다.")

except Exception as e:
    print(f"❌ 패치 중 오류 발생: {e}")