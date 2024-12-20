from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from movies.models import Movie

class MovieViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_movies(self):
        response = self.client.get(reverse('movie-list'))
        self.assertEqual(response.status_code, 200) 