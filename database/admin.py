from django.contrib import admin

from .models import Album, Music, Artist, Tag, Genre

class ArtistAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]
class MusicAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name',]

admin.site.register(Album)
admin.site.register(Music, MusicAdmin)
admin.site.register(Artist, ArtistAdmin)
admin.site.register(Tag)
admin.site.register(Genre)
