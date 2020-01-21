from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('music/', views.music, name="music"),
    path('portal/', views.portal, name="portal"),
    path('genres/', views.genres, name="genres"),
    path('genre/', views.genre, name="genre"),
    path('genre/<str:genre>/', views.genre, name="genre"),
    path('playlists/', views.playlists, name="playlists"),
    path('playlist/', views.playlist, name="playlist"),
    path('playlist/<int:playlist_id>/', views.playlist, name="playlist"),
    path('playlist-management/', views.playlistManagement, name="playlist-management")
]
