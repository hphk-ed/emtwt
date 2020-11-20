from rest_framework import serializers

from database.models import (
    Tag, 
    Hashtag,
    Music,
    Artist,
    Album,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'


class GetMusicSerializer(serializers.ModelSerializer):
    album = AlbumSerializer()
    class Meta:
        model = Music
        fields = '__all__'


class GetArtistSerializer(serializers.ModelSerializer):
    musics = MusicSerializer(many=True)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'musics', 'image')


class GetAlbumSerializer(serializers.ModelSerializer):
    music_set = MusicSerializer(many=True)
    class Meta:
        model = Album
        fields = ('id', 'title', 'image', 'release_date', 'music_set')


class GetMusicDetailSerializer(serializers.ModelSerializer):
    artists = GetArtistSerializer(many=True)
    album = GetAlbumSerializer()
    class Meta:
        model = Music
        fields = ('id', 'name', 'artists', 'lyrics', 'tags', 'fake_like', 'album', )

