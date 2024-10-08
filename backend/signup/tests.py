# tests.py
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.test import APITestCase
from core.models import CustomUser
from allauth.account.models import EmailAddress

# User signup and login tests
class UserSignUpTest(APITestCase):
    def setUp(self):
        self.signup_url = reverse('custom_signup')  # Adjust based on your URL naming
        self.login_url = reverse('login')  # Adjust based on your URL naming
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
        """Test signing up a user with valid data"""
        response = self.client.post(self.signup_url, self.valid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 2)
        self.assertEqual(CustomUser.objects.get(username='testuser').email, 'testuser@example.com')

    def test_signup_with_existing_email(self):
        """Test signing up a user with an email that's already registered"""
        response = self.client.post(self.signup_url, {**self.valid_user_data, 'email': self.existing_email}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email already registered.', response.data.get('email', ''))

    def test_signup_with_existing_username(self):
        """Test signing up a user with a username that's already taken"""
        response = self.client.post(self.signup_url, {**self.valid_user_data, 'username': self.existing_username}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username already taken. Be more creative.', response.data.get('username', ''))

    def test_signup_with_invalid_password(self):
        """Test signing up a user with an invalid password"""
        invalid_password_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'short',
            'password2': 'short',
        }
        response = self.client.post(self.signup_url, invalid_password_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Ensure this field has at least 8 characters.', response.data.get('password1', ''))

    def test_login_success(self):
        """Test logging in a user with valid credentials and email verified"""
        user = CustomUser.objects.create_user(username='loginuser', email='loginuser@example.com', password='password123')
        EmailAddress.objects.create(user=user, email='loginuser@example.com', verified=True)  # Email verified
        data = {'email': 'loginuser@example.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.cookies)
        self.assertIn('refresh', response.cookies)

    def test_login_with_wrong_password(self):
        """Test logging in with wrong password"""
        user = CustomUser.objects.create_user(username='loginuser', email='loginuser@example.com', password='password123')
        EmailAddress.objects.create(user=user, email='loginuser@example.com', verified=True)  # Email verified
        data = {'email': 'loginuser@example.com', 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Invalid credentials', response.json().get('detail', ''))

    def test_login_with_missing_email(self):
        """Test logging in without an email"""
        data = {'password': 'password123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email and password are required', response.json().get('detail', ''))

    def test_login_with_missing_password(self):
        """Test logging in without a password"""
        data = {'email': 'loginuser@example.com'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email and password are required', response.json().get('detail', ''))

    def test_login_with_unverified_email(self):
        """Test logging in without email verification"""
        user = CustomUser.objects.create_user(username='loginuser', email='loginuser@example.com', password='password123')
        # No email verification
        data = {'email': 'loginuser@example.com', 'password': 'password123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email is not verified', response.json().get('detail', ''))

    def test_login_with_invalid_email_format(self):
        """Test logging in with an invalid email format"""
        data = {'email': 'invalidemail', 'password': 'password123'}
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid email format', response.json().get('detail', ''))

# Custom user tests
class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword123'
        )

    def test_user_creation(self):
        """Test that a user can be created successfully."""
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_authentication(self):
        """Test that a user can authenticate with correct credentials."""
        authenticated_user = authenticate(email='test@example.com', password='testpassword123')
        self.assertEqual(authenticated_user, self.user)

    def test_user_authentication_failure(self):
        """Test that a user cannot authenticate with incorrect credentials."""
        authenticated_user = authenticate(email='test@example.com', password='wrongpassword')
        self.assertIsNone(authenticated_user)
