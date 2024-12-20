from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from movies.models import Movie, Review
from datetime import date

class ReviewAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            tmdb_id=12345,
            release_date=date.today()
        )
        self.client.force_authenticate(user=self.user)

    def test_create_review(self):
        data = {
            'movie': self.movie.id,
            'content': 'Great movie!',
            'rating': 5
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Review.objects.count(), 1)

    def test_like_review(self):
        review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            content='Test review',
            rating=4
        )
        response = self.client.post(f'/api/reviews/{review.id}/like/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(review.likes.count(), 1) 