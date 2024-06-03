# movies/models.py

from django.db import models
from django.contrib.auth.models import User

class MovieList(models.Model):
    name = models.CharField(max_length=100)
    is_public = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movie_lists')
    movies = models.ManyToManyField('Movie')

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    imdb_id = models.CharField(max_length=50, unique=True)
    year = models.CharField(max_length=4)
    poster = models.URLField(max_length=200, blank=True, null=True)  

    def __str__(self):
        return self.title
