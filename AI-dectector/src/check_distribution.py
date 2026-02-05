import json
import os

path_data = '/tmp/xdac_4de873bd_557xa6c0/XDAC_obs/LGC_data/LGC_data_v1.0.json'

with open(path_data, 'r', encoding='utf-8') as f:
    data_list = json.load(f)

lengths = [len(item.get('passage', '')) for item in data_list]
lengths.sort(reverse=True)

print(f"📊 데이터 길이 분석 (총 {len(data_list)}건)")
print(f"- 가장 긴 글: {lengths[0]}자")
print(f"- 상위 10% 길이: {lengths[len(lengths)//10]}자")
print(f"- 평균 길이: {sum(lengths)//len(lengths)}자")

# 300자 대신 '가장 긴 글들' 위주로 500건만 먼저 뽑아보기
min_len = 100 # 임시로 낮춤
ai_essays = [i for i in data_list if len(i.get('passage', '')) >= min_len]
print(f"✅ {min_len}자 이상 데이터: {len(ai_essays)}건")