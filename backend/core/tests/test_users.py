from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models import CustomUser

class UserModelTest(TestCase):
    def setUp(self):
        self.username = 'testUser2'
        self.email = 'testuser2@example.com'
        self.password = 'NewValidPassword123'
        self.user = CustomUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, self.username)
        self.assertTrue(self.user.check_password(self.password))

    def test_user_login(self):
        # Try with username
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        }, content_type='application/json')
        
        print(f"Username login - Status code: {response.status_code}")
        print(f"Username login - Response data: {response.json()}")

        # Try with email
        response_email = self.client.post(reverse('login'), {
            'email': self.email,
            'password': self.password
        }, content_type='application/json')
        
        print(f"Email login - Status code: {response_email.status_code}")
        print(f"Email login - Response data: {response_email.json()}")

        self.assertTrue(response.status_code == status.HTTP_200_OK or response_email.status_code == status.HTTP_200_OK)
        
        if response.status_code == status.HTTP_200_OK:
            self.assertIn('access', response.json())
        elif response_email.status_code == status.HTTP_200_OK:
            self.assertIn('access', response_email.json())