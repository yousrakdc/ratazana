from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from decimal import Decimal
from ..models import CustomUser, Jersey
from rest_framework_simplejwt.tokens import RefreshToken

class JerseyAPITest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testUser2',
            email='testuser2@example.com',
            password='NewValidPassword123'
        )

    def test_create_jersey(self):
        login_response = self.client.post('/auth/login/', {
            'email': 'testuser2@example.com',
            'password': 'NewValidPassword123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        access_token = login_response.json().get('access') 
        self.assertIsNotNone(access_token)

    def test_get_jersey_list(self):
        Jersey.objects.create(
            brand='Nike',
            team='Lakers',
            country='USA',
            color='Purple',
            price=Decimal('99.99'),
            sizes=['S', 'M'],
            image_path='path/to/image.jpg'
        )
        response = self.client.get(reverse('jersey-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class JerseyViewsTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testUser2',
            email='testuser2@example.com',
            password='NewValidPassword123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.jersey = Jersey.objects.create(
            brand='Nike',
            price=Decimal('100.00'),
            is_promoted=False,
            is_new_release=False,
            is_upcoming=False
        )

    def test_user_alert_creation(self):
        # Log in to get the access token
        login_response = self.client.post('/auth/login/', {
            'email': self.user.email,
            'password': 'NewValidPassword123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.json().get('access')
        self.assertIsNotNone(access_token)

        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.client.post('/api/alerts/', {
            'jersey_id': self.jersey.id, 
            'alert_type': 'price_drop',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_alert_creation_invalid(self):
        # Simulate a login request to get the access token
        login_response = self.client.post('/auth/login/', {
            'email': self.user.email,
            'password': 'NewValidPassword123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.json().get('access') 
        self.assertIsNotNone(access_token)

        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        response = self.client.post('/api/alerts/', {
            'alert_type': 'price_drop'
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view(self):
        # Simulate a login request with valid credentials
        response = self.client.post('/auth/login/', {
            'email': 'testuser2@example.com',
            'password': 'NewValidPassword123'
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.json())
        self.assertIn('refresh', response.cookies)

    def test_logout_view(self):
        login_response = self.client.post('/auth/login/', {
            'email': self.user.email,
            'password': 'NewValidPassword123'
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        access_token = login_response.json().get('access')
        self.assertIsNotNone(access_token)

        self.client.defaults['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        csrf_response = self.client.get('/api/csrf-token/')
        csrf_token = csrf_response.json().get('csrfToken')
        self.assertIsNotNone(csrf_token)

        refresh_token = login_response.cookies.get('refresh').value
        self.assertIsNotNone(refresh_token, "Refresh token should not be None")

        logout_response = self.client.post(
            '/auth/logout/',
            {'refresh': refresh_token}, 
            HTTP_X_CSRFTOKEN=csrf_token,
            HTTP_AUTHORIZATION=f'Bearer {access_token}' 
        )

        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        self.assertEqual(logout_response.json().get('message'), 'Logged out successfully.')