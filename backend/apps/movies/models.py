from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    runtime = models.PositiveIntegerField(null=True, blank=True)
    vote_average = models.FloatField(default=0)
    vote_count = models.PositiveIntegerField(default=0)
    popularity = models.FloatField(default=0)
    poster_url = models.URLField(blank=True)
    backdrop_url = models.URLField(blank=True)
    director = models.CharField(max_length=255, blank=True)
    cast = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies', blank=True)
    source_id = models.CharField(max_length=100, blank=True, unique=True)

    class Meta:
        ordering = ['-popularity', 'title']

    def __str__(self) -> str:
        return self.title


class UserRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movie_ratings')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')

# Create your models here.
