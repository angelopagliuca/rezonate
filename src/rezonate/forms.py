from django import forms
from .models import *

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ('audio', 'title', 'artist', 'image', 'lyrics', 'genre')

class DeleteSongForm(forms.Form):
    song = forms.ModelChoiceField(queryset=Song.objects.all(), to_field_name="title")

class AddRezonatorForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all().filter(rezonator__user__isnull=True))

class DeleteRezonatorForm(forms.Form):
    rezonator = forms.ModelChoiceField(queryset=User.objects.all().filter(rezonator__user__isnull=False))

class AddGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ('name', 'icon')

class DeleteGenreForm(forms.Form):
    genre = forms.ModelChoiceField(queryset=Genre.objects.all())

class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())

class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	first_name = forms.CharField(max_length=50)
	last_name = forms.CharField(max_length=50)
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=32, widget=forms.PasswordInput)

class AddPlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('songs', 'title', 'image')

class AddSongsToExistingPlaylist(forms.ModelForm):
    songs = forms.ModelMultipleChoiceField(queryset=Song.objects.all(), to_field_name="title", required=False)
    class Meta:
        model = Playlist
        fields = ('songs',)
