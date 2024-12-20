from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from movies.models import Movie, Review, UserProfile
from datetime import date

class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title="Test Movie",
            tmdb_id=12345,
            overview="Test overview",
            release_date=date.today()
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), "Test Movie")

    def test_poster_url(self):
        self.movie.poster_path = "/test.jpg"
        self.assertEqual(
            self.movie.poster_url,
            "https://image.tmdb.org/t/p/w500/test.jpg"
        )
        
    def test_poster_url_none(self):
        self.movie.poster_path = ""
        self.assertIsNone(self.movie.poster_url)

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title="Test Movie",
            tmdb_id=12345
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            content="Great movie!",
            rating=5
        )

    def test_review_str(self):
        expected = f'{self.movie.title} - 5/5 by {self.user.username}'
        self.assertEqual(str(self.review), expected)

    def test_invalid_rating(self):
        with self.assertRaises(ValidationError):
            review = Review(
                movie=self.movie,
                user=self.user,
                content="Test",
                rating=6
            )
            review.full_clean()

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.user.userprofile.bio, '') 