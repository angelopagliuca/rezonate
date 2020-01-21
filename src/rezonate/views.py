from django.shortcuts import render, redirect, reverse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.

def index(request):

    user = request.user

    if request.method == "POST":
        if "search" in request.POST:
            search_str = request.POST.get("searchbar")
            return music(request, search_str)

    data = {"user": user }
    return render(request, "index.html", data)

def music(request, search=""):
    user = request.user
    songs = Song.objects.all()

    if search != "":
        songs = Song.objects.filter(title__icontains=search)

    if request.method == "POST":
        if "search" in request.POST:
            search_str = request.POST.get("searchbar")
            songs = Song.objects.filter(title__icontains=search_str)
            songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)
            data = {"user": user, "songs": songs, "songs_json":songs_json, }
            return render(request, "music.html", data)

    songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)

    data = {"user": user, "songs": songs, "songs_json":songs_json, }
    return render(request, "music.html", data)

def genres(request):
    user = request.user

    genres = Genre.objects.all()

    data = {"user": user, "genres": genres,}
    return render(request, "genres.html", data)

def genre(request, genre=""):
    user = request.user

    genres = Genre.objects.all()

    redir = True
    for genrei in genres:
        if genre == genrei.name.lower():
            redir = False
    if redir: return redirect(reverse("genres"))

    genre = genre.lower().capitalize()
    songs = Song.objects.filter(genre__name=genre)

    if request.method == "POST":
        if "search" in request.POST:
            search_str = request.POST.get("searchbar")
            songs = Song.objects.filter(genre__name=genre, title__icontains=search_str)
            songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)
            data = {"user": user, "songs": songs, "songs_json":songs_json, }
            return render(request, "genre.html", data)

    songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)

    data = {"user": user, "songs": songs, "songs_json":songs_json,}
    return render(request, "genre.html", data)

def playlists(request):
    user = request.user
    playlists = Playlist.objects.all()
    if request.method == "POST":
        if "play-playlist" in request.POST:
            playlist = Playlist.objects.get(id=request.POST.get("play-playlist"))
            songs = playlist.songs.all()
            data = {"user": user, "songs": songs, "playlist": playlist}
            return redirect(reverse("music"), args=data)
    data = {"user": user, "playlists": playlists}
    return render(request, "playlists.html", data)

def playlist(request, playlist_id=0):
    user = request.user
    playlists = Playlist.objects.all()

    redir = True
    for playlist in playlists:
        if playlist_id == playlist.id:
            redir = False
    if redir: return redirect(reverse("playlists"))

    playlist = Playlist.objects.get(id=playlist_id)
    songs = playlist.songs.all()

    songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)

    if request.method == "POST":
        if "search" in request.POST:
            search_str = request.POST.get("searchbar")
            songs = songs.filter(title__icontains=search_str)
            songs_json = json.dumps(list(songs.values()), cls=DjangoJSONEncoder)
            data = {"user": user, "songs": songs, "songs_json":songs_json, }
            return render(request, "playlist.html", data)

    data = {"user": user, "songs": songs, "playlist": playlist, "songs_json":songs_json,}
    return render(request, "playlist.html", data)

@login_required(login_url='login')
def playlistManagement(request):
    user = request.user
    playlists = Playlist.objects.all().filter(user=user)
    add_song_form = SongForm()
    delete_song_form = DeleteSongForm()
    add_rezonator_form = AddRezonatorForm()
    delete_rezonator_form = DeleteRezonatorForm()
    user_form = UserForm()
    add_playlist_form = AddPlaylistForm()
    add_songs_to_playlist_form = AddSongsToExistingPlaylist()

    if request.method == "POST":
        if "add-playlist" in request.POST:
            form = AddPlaylistForm(request.POST, request.FILES)
            if form.is_valid():
                songs = form.cleaned_data["songs"]
                title = form.cleaned_data["title"]
                image = form.cleaned_data["image"]
                playlist = Playlist.objects.create(user=user, title=title, image=image)
                playlist.songs.set(songs)
                playlist.save()
        if "delete-playlist" in request.POST:
            playlist_id = request.POST.get("delete-playlist")
            Playlist.objects.filter(id=playlist_id).delete()
        if "deleteSongFromPlaylist" in request.POST:
            playlist_id = request.POST.get("deleteSong").split("[:]")[0]
            song_id = request.POST.get("deleteSong").split("[:]")[1]
            playlist = Playlist.objects.get(id=playlist_id)
            song = Song.objects.get(id=song_id)
            playlist.songs.remove(song)
        if "addSongsToPlaylist" in request.POST:
            form = AddSongsToExistingPlaylist(request.POST, request.FILES)
            playlist = Playlist.objects.get(id=request.POST.get("addSongsToPlaylist"))
            if form.is_valid():
                songs = form.cleaned_data["songs"]
                for song in songs:
                    playlist.songs.add(song)
                    playlist.save()

    data = {"user": user, "playlists": playlists, "add_song_form": add_song_form,
            "delete_song_form": delete_song_form,
            "delete_rezonator_form": delete_rezonator_form,
            "add_rezonator_form": add_rezonator_form,
            "user_form": user_form,
            "add_playlist_form": add_playlist_form,
            "add_songs_to_playlist_form": add_songs_to_playlist_form,}
    return render(request, "playlist-management.html", data)

# username: apagliuca, aparadkar, mtday
# password: 1234
@login_required(login_url='login')
def portal(request):

    user = request.user
    if not hasattr(user, 'rezonator'):
         return redirect(reverse('login'))

    add_song_form = SongForm()
    delete_song_form = DeleteSongForm()
    add_rezonator_form = AddRezonatorForm()
    delete_rezonator_form = DeleteRezonatorForm()
    add_genre_form = AddGenreForm()
    delete_genre_form = DeleteGenreForm()
    user_form = UserForm()
    add_playlist_form = AddPlaylistForm()

    if request.method == "POST":
        if "add-song" in request.POST:
            form = SongForm(request.POST, request.FILES)
            if form.is_valid():
                audio = form.cleaned_data["audio"]
                title = form.cleaned_data["title"]
                artist = form.cleaned_data["artist"]
                image = form.cleaned_data["image"]
                lyrics = form.cleaned_data["lyrics"]
                genre = form.cleaned_data["genre"]
                song = Song(audio=audio, title=title, artist=artist, image=image, lyrics=lyrics, genre=genre)
                song.save()
        if "delete-song" in request.POST:
            form = DeleteSongForm(request.POST, request.FILES)
            if form.is_valid():
                song = form.cleaned_data["song"]
                song.delete()
        if "add-genre" in request.POST:
            form = AddGenreForm(request.POST, request.FILES)
            if form.is_valid():
                add_genre = form.cleaned_data["name"]
                icon = form.cleaned_data["icon"]
                genre = Genre(name=add_genre, icon=icon)
                genre.save()
        if "delete-genre" in request.POST:
            form = DeleteGenreForm(request.POST, request.FILES)
            if form.is_valid():
                genre = form.cleaned_data["genre"]
                genre.delete()
        if "add-rezonator" in request.POST:
            form = AddRezonatorForm(request.POST, request.FILES)
            if form.is_valid():
                add_user = form.cleaned_data["user"]
                rezonator = Rezonator(user=add_user)
                rezonator.save()
        if "delete-rezonator" in request.POST:
            form = DeleteRezonatorForm(request.POST, request.FILES)
            if form.is_valid():
                delete_rez = form.cleaned_data["rezonator"]
                delete_rez.rezonator.delete()
        if "delete-user" in request.POST:
            form = UserForm(request.POST, request.FILES)
            if form.is_valid():
                delete_user = form.cleaned_data["user"]
                delete_user.delete()

    data = {"user": user, "add_song_form": add_song_form,
            "delete_song_form": delete_song_form,
            "delete_rezonator_form": delete_rezonator_form,
            "add_genre_form": add_genre_form, "delete_genre_form": delete_genre_form,
            "add_rezonator_form": add_rezonator_form, "user_form": user_form,}
    return render(request, "portal.html", data)

def register(request):

    user = request.user

    if request.method == "POST":
        if "register" in request.POST:
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                first_name = form.cleaned_data["first_name"]
                last_name = form.cleaned_data["last_name"]
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                try:
                    user = User.objects.create_user(username, None, password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect(reverse("index"))
                except:
                    return redirect(reverse("register"))

    data = {"user": user, }
    return render(request, "register.html", data)

def login_view(request):

    user = request.user

    if request.method == "POST":
        if "login" in request.POST:
            form = LoginForm(request.POST, request.FILES)
            if form.is_valid():
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(reverse("index"))
                else:
                    return redirect(reverse("login"))

    data = {"user": user, }
    return render(request, "login.html", data)

def logout_view(request):
    logout(request)
    return redirect(reverse("login"))
