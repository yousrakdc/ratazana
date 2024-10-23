from django.test import TestCase
from unittest.mock import patch
from core.models import Jersey, Alert, CustomUser
from core.tasks import send_email_notification, check_prices_and_notify, notify_price_drop
from decimal import Decimal


class EmailNotificationTaskTests(TestCase):
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

    @patch('core.tasks.send_email_via_gmail_api')
    def test_send_email_notification(self, mock_send_email):
        new_price = Decimal('89.99')
        send_email_notification(self.user.email, self.jersey.id, new_price)
        
        mock_send_email.assert_called_once_with(
            self.user.email,
            'RATAZANA Price Alert: Price Drop Notification!',
            f'The price for the Nike Lakers jersey has dropped! The new price is £{new_price}.'
        )

    @patch('core.tasks.send_email_notification')
    def test_notify_price_drop(self, mock_send_email_notification):
        new_price = Decimal('89.99')
        self.jersey.last_known_price = Decimal('99.99')
        self.jersey.save()

        notify_price_drop(self.jersey, new_price)
        mock_send_email_notification.delay.assert_called_once_with(
            self.user.email, self.jersey.id, new_price
        )

    @patch('core.tasks.Jersey.get_current_price')
    @patch('core.tasks.notify_price_drop')
    def test_check_prices_and_notify_price_drop(self, mock_notify_price_drop, mock_get_current_price):
        mock_get_current_price.return_value = Decimal('89.99')
        self.jersey.last_known_price = Decimal('99.99')
        self.jersey.save()

        check_prices_and_notify()

        mock_notify_price_drop.assert_called_once_with(self.jersey, Decimal('89.99'))
        self.jersey.refresh_from_db()
        self.assertEqual(self.jersey.last_known_price, Decimal('89.99'))

    @patch('core.tasks.Jersey.get_current_price')
    def test_check_prices_and_notify_no_price_drop(self, mock_get_current_price):
        mock_get_current_price.return_value = Decimal('100.00')
        self.jersey.last_known_price = Decimal('99.99')
        self.jersey.save()

        check_prices_and_notify()

        self.assertEqual(self.jersey.last_known_price, Decimal('99.99')) 

