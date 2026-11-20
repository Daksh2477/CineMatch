from django.db.models import Count, Q
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Genre, Movie, UserRating
from .serializers import GenreSerializer, MovieSerializer, RatingSerializer


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Movie.objects.prefetch_related('genres').all()
    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('q')
        genre = self.request.query_params.get('genre')
        year = self.request.query_params.get('year')
        rating = self.request.query_params.get('rating')
        ordering = self.request.query_params.get('ordering', '-popularity')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(description__icontains=search) | Q(director__icontains=search))
        if genre:
            queryset = queryset.filter(genres__slug=genre)
        if year:
            queryset = queryset.filter(release_year=year)
        if rating:
            queryset = queryset.filter(vote_average__gte=rating)
        if ordering in {'popularity', '-popularity', 'vote_average', '-vote_average', 'release_year', '-release_year', 'title', '-title'}:
            queryset = queryset.order_by(ordering)
        return queryset.distinct()

    @action(detail=False)
    def popular(self, request):
        movies = self.filter_queryset(self.get_queryset()).order_by('-popularity')[:20]
        return Response(MovieSerializer(movies, many=True).data)

    @action(detail=False)
    def search(self, request):
        search = request.query_params.get('q', '').strip()
        movies = self.get_queryset().filter(
            Q(title__icontains=search) | Q(description__icontains=search) | Q(director__icontains=search)
        )[:20] if search else []
        return Response(MovieSerializer(movies, many=True).data)


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Genre.objects.annotate(movie_count=Count('movies')).order_by('name')
    serializer_class = GenreSerializer


class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return UserRating.objects.filter(user=self.request.user).select_related('movie')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Create your views here.
