from django.db import models

# Create your models here.
# models.py

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
