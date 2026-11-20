from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

from apps.movies.models import Genre, Movie


class MovieApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.genre = Genre.objects.create(name='Science Fiction', slug='science-fiction')
        cls.movie = Movie.objects.create(
            title='Test Space',
            description='A crew explores a distant planet.',
            release_year=2024,
            runtime=120,
            vote_average=8.2,
            vote_count=500,
            popularity=90,
            source_id='test-1',
        )
        cls.movie.genres.add(cls.genre)

    def test_movie_list_supports_search_filtering(self):
        response = self.client.get('/api/movies/', {'q': 'Test', 'genre': 'science-fiction'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any(item['title'] == 'Test Space' for item in response.data['results']))

    def test_movie_detail_returns_title(self):
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Space')

    def test_invalid_movie_recommendation_returns_404(self):
        response = self.client.get('/api/recommendations/movie/99999/')
        self.assertEqual(response.status_code, 404)

    def test_authenticated_user_can_rate_movie(self):
        user = User.objects.create_user(username='viewer', password='strongpass123')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/ratings/', {'movie': self.movie.id, 'rating': 9})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['rating'], 9)

    def test_watchlist_rejects_missing_movie(self):
        user = User.objects.create_user(username='watcher', password='strongpass123')
        self.client.force_authenticate(user=user)
        response = self.client.post('/api/watchlist/', {'movie_id': 99999})
        self.assertEqual(response.status_code, 400)
