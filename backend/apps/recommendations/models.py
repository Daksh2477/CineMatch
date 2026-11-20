from django.conf import settings
from django.db import models

from apps.movies.models import Movie


class RecommendationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendation_history')
    source_movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, blank=True)
    mode = models.CharField(max_length=30)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
