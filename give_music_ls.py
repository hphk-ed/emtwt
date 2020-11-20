import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eds_music_travel_with_tony_back.settings")
django.setup()

from database.models import Music

all_music = Music.objects.all()

like_score_range = range(0, 2000)
for music in all_music:
    music.fake_like = random.sample(like_score_range, 1)[0]
    music.save()

    if music.id % 100 == 0:
        print(music.id)
