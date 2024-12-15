from tmdbv3api import TMDb, Movie as TMDBMovie
from django.conf import settings
from .models import Movie
from datetime import datetime

class TMDBService:
    def __init__(self):
        self.tmdb = TMDb()
        self.tmdb.api_key = settings.TMDB_API_KEY
        self.movie = TMDBMovie()

    def search_movies(self, query):
        return self.movie.search(query)

    def get_popular_movies(self):
        return self.movie.popular()

    def import_movie_to_db(self, tmdb_movie):
        movie, created = Movie.objects.get_or_create(
            tmdb_id=tmdb_movie.id,
            defaults={
                'title': tmdb_movie.title,
                'overview': getattr(tmdb_movie, 'overview', ''),
                'poster_path': getattr(tmdb_movie, 'poster_path', ''),
                'release_date': datetime.strptime(tmdb_movie.release_date, '%Y-%m-%d').date() if hasattr(tmdb_movie, 'release_date') else None
            }
        )
        return movie 