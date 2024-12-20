from django.test import TestCase
from unittest.mock import patch
from movies.services import TMDBService

class TMDBServiceTest(TestCase):
    @patch('tmdbv3api.Movie.search')
    def test_search_movies(self, mock_search):
        # Mock the TMDB API response
        mock_search.return_value = [
            type('TMDBMovie', (), {
                'id': 123,
                'title': 'Test Movie',
                'overview': 'Test overview',
                'poster_path': '/test.jpg',
                'release_date': '2024-01-01'
            })
        ]

        service = TMDBService()
        results = service.search_movies('test')
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Test Movie')

    @patch('tmdbv3api.Movie.popular')
    def test_get_popular_movies(self, mock_popular):
        mock_popular.return_value = [
            type('TMDBMovie', (), {
                'id': 456,
                'title': 'Popular Movie',
                'overview': 'Popular overview',
                'poster_path': '/popular.jpg',
                'release_date': '2024-01-01'
            })
        ]

        service = TMDBService()
        results = service.get_popular_movies()
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, 'Popular Movie') 