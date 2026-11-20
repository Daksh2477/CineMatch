from __future__ import annotations

from typing import Iterable

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from apps.movies.models import Movie


class RecommendationEngine:
     def __init__(self, movies: Iterable[Movie]):
         self.movies = list(movies)
         self.movie_ids = [movie.id for movie in self.movies]

     @staticmethod
     def _weighted_rating(movie: Movie, mean_rating: float, minimum_votes: int) -> float:
         vote_count = max(movie.vote_count, 0)
         return (
             (vote_count / (vote_count + minimum_votes)) * movie.vote_average
             + (minimum_votes / (vote_count + minimum_votes)) * mean_rating
         )

     def popular_movies(self, limit: int = 12) -> list[Movie]:
         if not self.movies:
             return []
         ratings = [movie.vote_average for movie in self.movies if movie.vote_average]
         mean_rating = float(np.mean(ratings)) if ratings else 0.0
         counts = [movie.vote_count for movie in self.movies if movie.vote_count]
         minimum_votes = int(np.percentile(counts, 70)) if counts else 0
         ranked = sorted(
             self.movies,
             key=lambda movie: self._weighted_rating(movie, mean_rating, minimum_votes),
             reverse=True,
         )
         return ranked[:limit]

     def genre_recommendations(self, genres: list[str], limit: int = 12) -> list[Movie]:
         if not genres:
             return self.popular_movies(limit)
         normalized = {genre.lower().strip() for genre in genres if genre.strip()}
         ranked = []
         for movie in self.movies:
             movie_genres = {genre.name.lower() for genre in movie.genres.all()}
             matches = len(normalized.intersection(movie_genres))
             if matches:
                 ranked.append((movie, matches))
         ranked.sort(
             key=lambda item: (
                 item[1],
                 item[0].vote_average,
                 item[0].popularity,
             ),
             reverse=True,
         )
         return [movie for movie, _ in ranked[:limit]]

     def similar_movies(self, selected: Movie, limit: int = 12) -> list[Movie]:
         if limit <= 0:
             return []
         if len(self.movies) < 2:
             return []
         corpus = [
             ' '.join(
                 [
                     movie.title,
                     movie.description,
                     ' '.join(genre.name for genre in movie.genres.all()),
                     movie.director,
                     movie.cast,
                     movie.keywords,
                 ]
             ).lower()
             for movie in self.movies
         ]
         vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
         matrix = vectorizer.fit_transform(corpus)
         try:
             selected_index = self.movie_ids.index(selected.id)
         except ValueError:
             return []
         similarities = cosine_similarity(matrix[selected_index], matrix).flatten()
         ranked_indices = np.argsort(-similarities)
         recommendations = []
         for index in ranked_indices:
             candidate = self.movies[int(index)]
             if candidate.id == selected.id:
                 continue
             recommendations.append(candidate)
             if len(recommendations) >= limit:
                 break
         return recommendations
