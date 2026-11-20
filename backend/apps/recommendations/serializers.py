from rest_framework import serializers

from apps.movies.serializers import MovieSerializer
from .models import RecommendationHistory


class PreferenceSerializer(serializers.Serializer):
    genres = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    limit = serializers.IntegerField(min_value=1, max_value=50, required=False, default=12)


class HistorySerializer(serializers.ModelSerializer):
    source_movie = MovieSerializer(read_only=True)

    class Meta:
        model = RecommendationHistory
        fields = ('id', 'source_movie', 'mode', 'preferences', 'created_at')
