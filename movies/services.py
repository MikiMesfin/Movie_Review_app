from tmdbv3api import TMDb, Movie as TMDBMovie
from django.conf import settings
from .models import Movie

tmdb = TMDb()
tmdb.api_key = settings.TMDB_API_KEY  # Instead of hardcoded value
movie_api = TMDBMovie()

class TMDBService:
    @staticmethod
    def search_movies(query):
        try:
            return movie_api.search(query)
        except Exception as e:
            print(f"TMDB API Error: {str(e)}")
            return []

    @staticmethod
    def get_popular_movies():
        try:
            return movie_api.popular()
        except Exception as e:
            print(f"TMDB API Error: {str(e)}")
            return []

    @staticmethod
    def get_movie_details(tmdb_id):
        return movie_api.details(tmdb_id)

    @staticmethod
    def import_movie_to_db(tmdb_movie):
        try:
            movie, created = Movie.objects.get_or_create(
                tmdb_id=tmdb_movie.id,  # Changed from title to tmdb_id for uniqueness
                defaults={
                    'title': tmdb_movie.title,
                    'overview': getattr(tmdb_movie, 'overview', ''),
                    'poster_path': getattr(tmdb_movie, 'poster_path', ''),
                    'release_date': getattr(tmdb_movie, 'release_date', None)
                }
            )
            return movie
        except Exception as e:
            print(f"Database Error: {str(e)}")
            return None 