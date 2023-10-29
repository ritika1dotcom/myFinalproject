from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    # Other song attributes if necessary

class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    album_image = models.URLField(max_length=500, null=True, blank=True)  # New field for album image URL
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.song_title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='static/images/')