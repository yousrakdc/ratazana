from django.test import TestCase
from core.models import Alert, Jersey
from ..models import CustomUser
from decimal import Decimal

class AlertModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='securepassword123'
        )
        self.jersey = Jersey.objects.create(
            brand='Nike',
            team='Lakers',
            price=Decimal('99.99'),
            last_known_price=Decimal('99.99')
        )
        self.alert = Alert.objects.create(
            user=self.user,
            jersey=self.jersey,
            alert_type='price_drop',
            status='active'
        )

    def test_alert_creation(self):
        self.assertEqual(self.alert.jersey.team, 'Lakers')
        self.assertEqual(self.alert.alert_type, 'price_drop')

    def test_trigger_alert(self):
        self.alert.trigger_alert()
        self.assertEqual(self.alert.status, 'triggered')
