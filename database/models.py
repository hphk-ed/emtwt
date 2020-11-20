from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.TextField(blank=True, default='')
    flo_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=100)
    image = models.TextField(blank=True, default='')
    release_date = models.DateField()
    flo_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.title
        

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=100)
    lyrics = models.TextField(blank=True, default='')
    artists = models.ManyToManyField(Artist, related_name='musics')
    featuring_artists = models.ManyToManyField(Artist, related_name='featuring_musics', blank=True)
    genres = models.ManyToManyField(Genre, related_name='musics')
    album = models.ForeignKey(Album, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='musics', blank=True)
    flo_id = models.IntegerField(blank=True, default=0)

    fake_like = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.pk}. {self.name}'


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    content = models.TextField(null=True)
    score = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(Hashtag, related_name='reviews')

    def __str__(self):
        return f'{self.id}: '
