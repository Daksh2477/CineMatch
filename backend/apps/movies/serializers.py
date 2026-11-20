from rest_framework import serializers

from .models import Genre, Movie, UserRating


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        source='genres',
        write_only=True,
        required=False,
    )

    class Meta:
        model = Movie
        fields = (
            'id', 'title', 'description', 'release_year', 'runtime',
            'vote_average', 'vote_count', 'popularity', 'poster_url',
            'backdrop_url', 'director', 'cast', 'keywords', 'genres',
            'genre_ids', 'source_id',
        )


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ('id', 'movie', 'rating', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def validate_rating(self, value: int) -> int:
        if not 1 <= value <= 10:
            raise serializers.ValidationError('Rating must be between 1 and 10.')
        return value
