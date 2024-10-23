from django.test import TestCase
from decimal import Decimal
from ..models import Jersey

class JerseyModelTest(TestCase):
    def setUp(self):
        self.jersey = Jersey.objects.create(
            brand='Nike',
            team='Sample Jersey',
            price=Decimal('100.00'),
            is_promoted=False
        )

    def test_jersey_creation(self):
        self.assertEqual(self.jersey.team, 'Sample Jersey')
        self.assertEqual(self.jersey.price, Decimal('100.00'))
        self.assertFalse(self.jersey.is_promoted)

    def test_jersey_price_update(self):
        self.jersey.price = Decimal('150.00')
        self.jersey.save()
        self.assertEqual(self.jersey.price, Decimal('150.00'))
