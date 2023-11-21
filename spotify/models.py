from django.db import models

# Create your models here.
# models.py
class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    album = models.CharField(max_length=255, default=None)
    file_path = models.FileField(upload_to='static/songs/')

    def __str__(self):
        return self.title
