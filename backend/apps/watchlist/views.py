from rest_framework import permissions, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.movies.models import Movie
from .models import WatchlistItem
from .serializers import WatchlistSerializer


class WatchlistViewSet(viewsets.ModelViewSet):
    queryset = WatchlistItem.objects.all()
    serializer_class = WatchlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return WatchlistItem.objects.filter(user=self.request.user).select_related('movie').prefetch_related('movie__genres')

    def create(self, request, *args, **kwargs):
        movie_id = request.data.get('movie_id')
        try:
            movie = Movie.objects.get(pk=movie_id)
        except (Movie.DoesNotExist, TypeError, ValueError):
            raise ValidationError({'movie_id': 'A valid movie ID is required.'})
        item, created = WatchlistItem.objects.get_or_create(user=request.user, movie=movie)
        http_status = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(WatchlistSerializer(item, context={'request': request}).data, status=http_status)

# Create your views here.
