"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.movies.views import GenreViewSet, MovieViewSet, RatingViewSet
from apps.recommendations.views import HistoryViewSet, RecommendationViewSet
from apps.users.views import RegisterView
from apps.watchlist.views import WatchlistViewSet

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movie')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'ratings', RatingViewSet, basename='rating')
router.register(r'watchlist', WatchlistViewSet, basename='watchlist')
router.register(r'history', HistoryViewSet, basename='history')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path(
        'api/recommendations/movie/<int:pk>/',
        RecommendationViewSet.as_view({'get': 'movie'}),
    ),
    path(
        'api/recommendations/preferences/',
        RecommendationViewSet.as_view({'post': 'preferences'}),
    ),
    path('api/auth/register/', RegisterView.as_view()),
    path('api/auth/token/', TokenObtainPairView.as_view()),
    path('api/auth/token/refresh/', TokenRefreshView.as_view()),
    path('api/schema/', SpectacularAPIView.as_view()),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
]
