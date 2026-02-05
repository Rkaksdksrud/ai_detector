import os

target_file = '/home/ktg0310/ml_project/AI-dectector/XDAC_obs/xdac_encrypted.py'
# 바이너리 패턴 정의 (./XDAC-D)
old_pattern = b"./XDAC-D"
# 새로운 절대 경로 패턴 (길이가 다르면 파일이 깨질 수 있으므로 패딩이나 엔진 내부 로직을 고려해야 함)
new_pattern = b"/home/ktg0310/ml_project/AI-dectector/XDAC_obs/XDAC-D"

if not os.path.exists(target_file):
    print(f"❌ 파일을 찾을 수 없습니다.")
    exit()

print(f"🛠️ 바이너리 레벨 패치 시도 중...")

try:
    with open(target_file, 'rb') as f:
        content = f.read()

    if old_pattern in content:
        # 문자열 치환 후 다시 쓰기
        new_content = content.replace(old_pattern, new_pattern)
        with open(target_file, 'wb') as f:
            f.write(new_content)
        print(f"✅ 바이너리 패치 성공! 패턴을 교체했습니다.")
    else:
        print("❌ 바이너리 데이터 내에서도 './XDAC-D' 패턴을 찾지 못했습니다.")
        print("💡 힌트: 엔진이 내부에서 'XDAC-D' 문자열을 결합해서 만들고 있을 수 있습니다.")
except Exception as e:
    print(f"❌ 오류 발생: {e}")