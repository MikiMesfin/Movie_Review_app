from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_jwt_token_obtain(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_jwt_token_refresh(self):
        # First obtain tokens
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': self.user_data['username'],
            'password': self.user_data['password']
        })
        refresh_token = response.data['refresh']

        # Then try to refresh the access token
        response = self.client.post(reverse('token_refresh'), {
            'refresh': refresh_token
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data) 