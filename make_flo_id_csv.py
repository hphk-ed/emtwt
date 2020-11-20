import requests
import csv

size = 50
keyword_list = [
    "운동할 때", "데이트", "출근", "퇴근", 
    "여행", "노동요", "명상", "식사할 때",
]

keyword = '걸그룹'
API_URL = f"https://www.music-flo.com/api/search/v2/search?keyword={keyword}&searchType=ESALBUM&sortType=POPULAR&size={size}"
THEME_URL = "http://music-flo.com/api/meta/v1/channel/"

playlist_resp = requests.get(API_URL).json()
# 플레이 리스트 정보 GET
playlist = playlist_resp.get('data').get('list')[0].get('list')
# print(len(playlist))

# 각 플레이 리스트들의 접근 ID 를 추출 및 노래 목록 가져오기
# ml = []
with open('music_flo_id.csv', 'w', encoding='utf-8', newline="") as f:
    for p in playlist:
        # print(p.get('id'), p.get('name'), f"{THEME_URL}{p.get('id')}")
        music_res = requests.get(f"{THEME_URL}{p.get('id')}").json()
        musiclist = music_res.get('data').get('trackList')
        # 뮤직 내용을 저장 하는 부분이 필요.
            # print(musiclist)
        for music in musiclist:
            wt = csv.writer(f, delimiter='|')
            wt.writerow([music.get('id'), music.get('name')])

        