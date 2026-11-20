from django.test import TestCase

from apps.movies.models import Genre, Movie
from apps.recommendations.engine import RecommendationEngine


class RecommendationEngineTests(TestCase):
    def setUp(self):
        sci_fi = Genre.objects.create(name='Sci-Fi', slug='sci-fi')
        drama = Genre.objects.create(name='Drama', slug='drama')
        self.interstellar = Movie.objects.create(
            title='Interstellar', description='space time travel', release_year=2014,
            vote_average=8.4, vote_count=30000, popularity=95, source_id='space-1',
        )
        self.mars = Movie.objects.create(
            title='The Martian', description='astronaut Mars survival', release_year=2015,
            vote_average=8.0, vote_count=22000, popularity=89, source_id='space-2',
        )
        self.comedy = Movie.objects.create(
            title='A Comedy', description='friends and a family holiday', release_year=2018,
            vote_average=7.2, vote_count=100, popularity=40, source_id='comedy-1',
        )
        self.interstellar.genres.add(sci_fi, drama)
        self.mars.genres.add(sci_fi, drama)

    def test_content_recommendation_returns_related_movie_and_not_source(self):
        engine = RecommendationEngine(Movie.objects.prefetch_related('genres').all())
        results = engine.similar_movies(self.interstellar, limit=5)
        self.assertNotIn(self.interstellar, results)
        self.assertIn(self.mars, results)

    def test_genre_recommendation_is_not_random(self):
        engine = RecommendationEngine(Movie.objects.prefetch_related('genres').all())
        results = engine.genre_recommendations(['Sci-Fi'], limit=5)
        self.assertTrue(results)
        self.assertNotIn(self.comedy, results)

    def test_empty_dataset_and_result_limit_are_safe(self):
        engine = RecommendationEngine([])
        self.assertEqual(engine.popular_movies(), [])
        self.assertEqual(engine.genre_recommendations(['Drama']), [])
        self.assertEqual(engine.similar_movies(self.interstellar, limit=0), [])
