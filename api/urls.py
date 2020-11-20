from django.urls import path

from . import views


urlpatterns = [
    path('tags/', views.tag_list),
    path('hashtags/', views.hashtag_list),
    path('tags/<int:tag_pk>/', views.tag_detail),
    path('music/<int:music_pk>/', views.music_detail_create),
    path('artist/<int:artist_pk>/', views.artist_detail),
    path('album/<int:album_pk>/', views.album_detail),
    path('search/<str:keyword>/', views.search),
]
