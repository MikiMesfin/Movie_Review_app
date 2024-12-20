from django.test import TestCase
from django.contrib.auth.models import User
from movies.models import Movie, Review
from movies.serializers import MovieSerializer, ReviewSerializer, UserSerializer
from datetime import date

class MovieSerializerTest(TestCase):
    def setUp(self):
        self.movie_data = {
            'title': 'Test Movie',
            'tmdb_id': 12345,
            'overview': 'Test overview',
            'release_date': date.today()
        }
        self.movie = Movie.objects.create(**self.movie_data)
        self.serializer = MovieSerializer(instance=self.movie)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'title', 'tmdb_id', 'overview', 'poster_url',
             'release_date', 'created_at', 'updated_at']
        )

class ReviewSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            tmdb_id=12345
        )
        self.review_data = {
            'movie': self.movie,
            'user': self.user,
            'content': 'Great movie!',
            'rating': 5
        }
        self.review = Review.objects.create(**self.review_data)
        self.serializer = ReviewSerializer(instance=self.review)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(
            data.keys(),
            ['id', 'movie', 'user', 'content', 'rating', 'created_at', 'likes_count']
        ) 