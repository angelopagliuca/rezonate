from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=50, default="")
    icon = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.name

class Song(models.Model):
    audio = models.FileField(null=True, validators=[FileExtensionValidator(allowed_extensions=['mp3'])])
    title = models.CharField(max_length=100, default="")
    artist = models.CharField(max_length=100, default="")
    image = models.FileField(null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    lyrics = models.FileField(default='_default_lyrics.txt', validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    class Meta:
        verbose_name = ("song")
        verbose_name_plural = ("songs")
    def __str__(self):
        return self.title

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=None)
    title = models.CharField(max_length=100, default="")
    songs = models.ManyToManyField(Song)
    image = models.FileField(null=True, blank=True, default="")
    def __str__(self):
        return self.title

class Rezonator(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=None)
