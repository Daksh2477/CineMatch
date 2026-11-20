from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.movies.models import Movie
from apps.movies.serializers import MovieSerializer
from .models import RecommendationHistory
from .serializers import HistorySerializer, PreferenceSerializer
from .engine import RecommendationEngine


class RecommendationViewSet(viewsets.ViewSet):
    serializer_class = PreferenceSerializer
    @action(detail=False, methods=['post'], url_path='preferences')
    def preferences(self, request):
        serializer = PreferenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        engine = RecommendationEngine(Movie.objects.prefetch_related('genres').all())
        recommendations = engine.genre_recommendations(
            serializer.validated_data['genres'],
            serializer.validated_data['limit'],
        )
        if request.user.is_authenticated:
            RecommendationHistory.objects.create(
                user=request.user,
                mode='genre',
                preferences={'genres': serializer.validated_data['genres']},
            )
        return Response([MovieSerializer(movie).data for movie in recommendations])

    @action(detail=True, methods=['get'], url_path='movie')
    def movie(self, request, pk=None):
        try:
            movie = Movie.objects.prefetch_related('genres').get(pk=pk)
        except Movie.DoesNotExist:
            return Response({'detail': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)
        limit = min(max(int(request.query_params.get('limit', 12)), 1), 50)
        engine = RecommendationEngine(Movie.objects.prefetch_related('genres').all())
        recommendations = engine.similar_movies(movie, limit)
        if request.user.is_authenticated:
            RecommendationHistory.objects.create(user=request.user, source_movie=movie, mode='content')
        return Response([MovieSerializer(item).data for item in recommendations])

    @action(detail=False, methods=['get'])
    def popular(self, request):
        engine = RecommendationEngine(Movie.objects.prefetch_related('genres').all())
        return Response([MovieSerializer(movie).data for movie in engine.popular_movies()])


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RecommendationHistory.objects.all()
    serializer_class = HistorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return RecommendationHistory.objects.filter(user=self.request.user).select_related('source_movie')

# Create your views here.
