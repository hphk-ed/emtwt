import csv
import json
import requests

with open('music_flo_id.csv', 'r', encoding='utf-8', newline="") as f:
    spamreader = csv.reader(f)
    data = []
    for row in spamreader:
        flo_id = row[0].split('|')[0]
        response = requests.get(f'https://www.music-flo.com/api/meta/v1/track/{flo_id}').json()
        name = response.get('data').get('name')
        lyrics = response.get('data').get('lyrics')
        artists = response.get('data').get('artistList')

        data.append({
            'name': name,
            'lyrics': lyrics,
            'artists': artists,
        })

    # with open('dump.json', 'a', encoding='utf-8', newline="") as rf:
    #     json.dump(data, rf, indent=2, ensure_ascii=False)