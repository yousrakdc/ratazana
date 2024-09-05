from django.test import TestCase
from core.models import CustomUser

class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')