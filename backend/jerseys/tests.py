import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from jerseys.models import Jersey

class PromotedJerseysAPITest(APITestCase):

    def setUp(self):
        Jersey.objects.create(name="Team A Home", team="Team A", season="2023", is_promoted=True, price=10.0)
        Jersey.objects.create(name="Team B Away", team="Team B", season="2023", is_promoted=False, price=15.0)
        Jersey.objects.create(name="Team C Third", team="Team C", season="2023", is_promoted=True, price=20.0)

    def test_get_promoted_jerseys(self):
        url = reverse('promoted-jerseys')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the response data is a dictionary
        self.assertIsInstance(response.data, dict)

        # Access the list inside the dictionary
        promoted_jerseys = response.data.get('promoted_jerseys', [])

        # Ensure the promoted_jerseys is a list
        self.assertIsInstance(promoted_jerseys, list)

        promoted_jerseys_count = Jersey.objects.filter(is_promoted=True).count()
        self.assertEqual(len(promoted_jerseys), promoted_jerseys_count)

        jersey_names = [jersey['name'] for jersey in promoted_jerseys]
        self.assertIn("Team A Home", jersey_names)
        self.assertIn("Team C Third", jersey_names)
        self.assertNotIn("Team B Away", jersey_names)

    def test_no_promoted_jerseys(self):
        Jersey.objects.all().delete()
        url = reverse('promoted-jerseys')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the response data is a dictionary
        self.assertIsInstance(response.data, dict)

        # Access the list inside the dictionary
        promoted_jerseys = response.data.get('promoted_jerseys', [])

        # Ensure the promoted_jerseys is a list
        self.assertIsInstance(promoted_jerseys, list)

        self.assertEqual(len(promoted_jerseys), 0)

    def test_mixed_promoted_jerseys(self):
        Jersey.objects.create(name="Team D Away", team="Team D", season="2023", is_promoted=False, price=25.0)
        url = reverse('promoted-jerseys')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Ensure the response data is a dictionary
        self.assertIsInstance(response.data, dict)

        # Access the list inside the dictionary
        promoted_jerseys = response.data.get('promoted_jerseys', [])

        # Ensure the promoted_jerseys is a list
        self.assertIsInstance(promoted_jerseys, list)

        jersey_names = [jersey['name'] for jersey in promoted_jerseys]
        self.assertNotIn("Team D Away", jersey_names)
        self.assertIn("Team A Home", jersey_names)
        self.assertIn("Team C Third", jersey_names)
