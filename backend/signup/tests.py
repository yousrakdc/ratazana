from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import CustomUser

class UserSignUpTest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('custom_signup')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'ValidPassword123',
            'password2': 'ValidPassword123',
        }
        self.existing_email = 'existing@example.com'
        self.existing_username = 'existinguser'
        CustomUser.objects.create_user(username=self.existing_username, email=self.existing_email, password='ValidPassword123')

    def test_signup_with_valid_data(self):
        response = self.client.post(self.signup_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username='testuser').email, 'testuser@example.com')

    def test_signup_with_existing_email(self):
        response = self.client.post(self.signup_url, {**self.valid_user_data, 'email': self.existing_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email already registered.', response.data.get('email', ''))

    def test_signup_with_existing_username(self):
        response = self.client.post(self.signup_url, {**self.valid_user_data, 'username': self.existing_username}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username already taken. Be more creative.', response.data.get('username', ''))

    def test_signup_with_invalid_password(self):
        invalid_password_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'short',
            'password2': 'short',
        }
        response = self.client.post(self.signup_url, invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ensure this field has at least 8 characters.', response.data.get('password1', ''))
