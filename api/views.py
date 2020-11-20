from django.shortcuts import render, get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND
)

from database.models import (
    Tag, 
    Hashtag,
    Music,
    Artist,
    Album,
)
from .serializers import (
    TagSerializer, 
    HashtagSerializer,
    ArtistSerializer,
    MusicSerializer,
    AlbumSerializer,
    GetMusicSerializer,
    GetMusicDetailSerializer,
    GetArtistSerializer,
    GetAlbumSerializer,
)


@api_view(['GET', 'POST'])
def tag_list(request):
    if request.method == "POST":
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        tag_list = Tag.objects.all()
        serializer = TagSerializer(tag_list, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def hashtag_list(request):
    if request.method == "POST":
        serializer = HashtagSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
    else:
        hashtags = Hashtag.objects.all()
        serializer = HashtagSerializer(hashtags, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def music_detail_create(request, music_pk):
    if request.method == 'GET':
        music = get_object_or_404(Music, pk=music_pk)
        serializer = GetMusicDetailSerializer(music)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MusicSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['GET'])
def tag_detail(request, tag_pk):
    tag = get_object_or_404(Tag, pk=tag_pk)
    if request.method == 'GET':
        musics_data = []
        for music in tag.musics.order_by('-fake_like')[:10]:
            artist = music.artists.all()[0]
            row_data = GetMusicSerializer(music).data
            row_data.update({
                'image': music.album.image,
                'artist': GetArtistSerializer(artist).data,
            })
            
            musics_data.append(row_data)
        context = {
            'name': tag.name,
            'musics': musics_data
        }
        return Response(context)
    else:
        pass


@api_view(['GET'])
def artist_detail(request, artist_pk):
    artist = get_object_or_404(Artist, id=artist_pk)
    artist_data = GetArtistSerializer(artist).data
    return Response(artist_data)


@api_view(['GET'])
def album_detail(request, album_pk):
    album = get_object_or_404(Album, pk=album_pk)
    album_music = album.music_set.first()
    if album_music:
        album_artist = ArtistSerializer(album_music.artists.first()).data
        album_data = GetAlbumSerializer(album).data
        album_data.update({'artist':album_artist})
        return Response(album_data)
    return Response(status=HTTP_404_NOT_FOUND)


@api_view(['GET'])
def search(request, keyword):
    musics = Music.objects.filter(name__icontains=keyword).order_by('-fake_like')[:10]
    artists = Artist.objects.filter(name__icontains=keyword)
    albums = Album.objects.filter(title__icontains=keyword)
    tags = Tag.objects.filter(name__icontains=keyword)
    
    context = {
        'musics': MusicSerializer(musics, many=True).data,
        'artists': ArtistSerializer(artists, many=True).data,
        'albums': AlbumSerializer(albums, many=True).data,
        'tags': TagSerializer(tags, many=True).data,
    }
    return Response(context)
