from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from movies.permissions import IsOwnerOrReadOnly
from movies.models import Review, Movie

class IsOwnerOrReadOnlyTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            username='owner',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='other',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            title='Test Movie',
            tmdb_id=12345
        )
        self.review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            content='Test review',
            rating=5
        )
        self.permission = IsOwnerOrReadOnly()

    def test_owner_can_edit(self):
        request = self.factory.put('/fake-url/')
        request.user = self.user
        self.assertTrue(
            self.permission.has_object_permission(request, None, self.review)
        )

    def test_non_owner_cannot_edit(self):
        request = self.factory.put('/fake-url/')
        request.user = self.other_user
        self.assertFalse(
            self.permission.has_object_permission(request, None, self.review)
        )

    def test_anyone_can_read(self):
        request = self.factory.get('/fake-url/')
        request.user = self.other_user
        self.assertTrue(
            self.permission.has_object_permission(request, None, self.review)
        ) 