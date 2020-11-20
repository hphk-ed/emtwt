import os
import django
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eds_music_travel_with_tony_back.settings")
django.setup()


from database.models import Music, Album, Artist, Tag, Genre

from django.core import serializers

XMLSerializer = serializers.get_serializer("json")
xml_serializer = XMLSerializer()

model_list = [
    *Music.objects.all(),
    *Album.objects.all(),
    *Artist.objects.all(),
    *Tag.objects.all(),
    *Genre.objects.all(),
]
data = serializers.serialize('json', model_list)

with open("flodata.json", "w", encoding='utf-8') as out:
    out.write(data)
    