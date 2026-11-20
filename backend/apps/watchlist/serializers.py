from rest_framework import serializers

from apps.movies.serializers import MovieSerializer
from .models import WatchlistItem


class WatchlistSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)
    movie_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = WatchlistItem
        fields = ('id', 'movie', 'movie_id', 'created_at')
        read_only_fields = ('id', 'created_at')
