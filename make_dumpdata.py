# -*- coding:utf-8 -*-
import requests
import json
import os
import django
import re
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eds_music_travel_with_tony_back.settings")
django.setup()


from database.models import Music, Album, Artist, Tag, Genre


def save_album_info(album_data):
    title = album_data.get('title')
    flo_id = album_data.get('id')
    # /dims/resize/75x75/quality/90' 여기서 resize 만 변경하면 원하는 사이즈가 나옴.
    # print(re.split('\?', img))
    img_url = re.split('\?', album_data.get('imgList')[0].get('url'))[0]

    releaseYmd = album_data.get('releaseYmd')
    try:
        releaseYmd = datetime.strptime(releaseYmd, '%Y%m%d')
    except:
        # 옛날 곡은 년월일 이 아닌 년월 혹은 년으로 되어 있음. ex) 19980000, 199901, 1978
        releaseYmd = datetime.strptime(releaseYmd.strip()[:4], '%Y')

    album, _ = Album.objects.get_or_create(title=title, image=img_url, release_date=releaseYmd, flo_id=flo_id)
    
    return album


def save_artists_info(artists_data):
    artist_list = []
    for artist in artists_data:
        name = artist.get('name')
        flo_id = artist.get('id')
        try:
            res = requests.get(f'http://music-flo.com/api/meta/v1/artist/{flo_id}').json()
        except:
            res = requests.get(f'http://music-flo.com/api/meta/v1/artist/{flo_id}').json()
            
        img_url = re.split('\?', res.get('data').get('imgList')[0].get('url'))[0]
        # print(name, flo_id, img_url)
        save_data, _ = Artist.objects.get_or_create(name=name, flo_id=flo_id, image=img_url)
        artist_list.append(save_data)

    return artist_list


def get_lyric_genre(music_id):
    MUSIC_URL = f'https://www.music-flo.com/api/meta/v1/track/{music_id}'
    response = requests.get(MUSIC_URL).json()
    data = response.get('data')
    if not data:
        return '', []
    lyrics = data.get('lyrics')
    genre_list = data.get('album').get('genreStyle').split(',')
    
    genres = []
    for genre_name in genre_list:
        genre, _ = Genre.objects.get_or_create(name=genre_name)
        genres.append(genre)

    return lyrics or "", genres


def make_seed_db(tag, size=50):

    keyword = tag.name
    print(keyword)
    API_URL = f"https://www.music-flo.com/api/search/v2/search?keyword={keyword}&searchType=ESALBUM&sortType=POPULAR&size={size}"
    THEME_URL = "http://music-flo.com/api/meta/v1/channel/"

    playlist_resp = requests.get(API_URL).json()
    # 플레이 리스트 정보 GET
    playlist = playlist_resp.get('data').get('list')[0].get('list')
    
    # 각 플레이 리스트들의 접근 ID 를 추출 및 노래 목록 가져오기
    for p in playlist:
        # JSON Decoder 에러 발생으로 두 번 요청.
        try:
            music_res = requests.get(f"{THEME_URL}{p.get('id')}").json()
        except:
            music_res = requests.get(f"{THEME_URL}{p.get('id')}").json()

        music_list = music_res.get('data').get('trackList')
        # 뮤직 내용을 저장 하는 부분이 필요.
            
        for music in music_list:
            # 앨범 정보 저장
            album = save_album_info(music.get('album'))
            # 가수 정보 저장
            artist_list = save_artists_info(music.get('artistList'))
            # 노래 정보 저장
            name = music.get('name')
            music_id = music.get('id')
            if not Music.objects.filter(flo_id=music_id):
                lyrics, genre_list = get_lyric_genre(music_id)
                new_music = Music()
                new_music.name = name
                new_music.flo_id = music_id
                new_music.album = album
                new_music.lyrics = lyrics
                
                new_music.save() # many to many 저장하기위해 id가 필요하므로 우선 저장.

                for artist in artist_list:
                    new_music.artists.add(artist)

                for genre in genre_list:
                    new_music.genres.add(genre)

                tag = Tag.objects.get(name=keyword)
                new_music.tags.add(tag)

                new_music.save()


keyword_list = [
    # "운동할 때", 
    # "출근",
    # "퇴근", 
    # "여행", 
    # "노동요", 
    # "명상", 
    # "식사할 때",
    # "데이트",
    # '외로움',
    # '카페',
    # '디즈니',
    # '영화OST',
    # '드라마OST',
    # '크리스마스',
    # '연말',
    # '코딩',
    '봄',
    # '여름',
    # '가을',
    # '겨울',
    # '힐링',
    # '팝송',
    # '7080',
    # '8090',
    # '감성',
]

for key in keyword_list:
    tag, _ = Tag.objects.get_or_create(name=key)
    make_seed_db(tag)
