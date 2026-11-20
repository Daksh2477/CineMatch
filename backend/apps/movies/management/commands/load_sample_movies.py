import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from apps.movies.models import Genre, Movie


class Command(BaseCommand):
    help = 'Load the bundled CineMatch demo movie dataset.'

    def handle(self, *args, **options):
        csv_path = Path(__file__).resolve().parents[4] / 'datasets' / 'sample_movies.csv'
        created_movies = 0
        with csv_path.open('r', encoding='utf-8', newline='') as handle:
            for row in csv.DictReader(handle):
                defaults = {
                    'description': row['description'].strip(),
                    'release_year': int(row['release_year']),
                    'runtime': int(row['runtime']),
                    'vote_average': float(row['vote_average']),
                    'vote_count': int(row['vote_count']),
                    'popularity': float(row['popularity']),
                    'director': row['director'].strip(),
                    'cast': row['cast'].strip(),
                    'keywords': row['keywords'].strip(),
                    'poster_url': (row.get('poster_url') or '').strip(),
                }
                movie, created = Movie.objects.update_or_create(
                    source_id=row['source_id'],
                    defaults={**defaults, 'title': row['title'].strip()},
                )
                genres = []
                for name in row['genres'].split('|'):
                    name = name.strip()
                    genre, _ = Genre.objects.get_or_create(
                        name=name,
                        defaults={'slug': name.lower().replace(' ', '-')},
                    )
                    genres.append(genre)
                movie.genres.set(genres)
                created_movies += int(created)
        self.stdout.write(self.style.SUCCESS(f'Demo dataset loaded. Movies: {Movie.objects.count()}, newly created: {created_movies}.'))
