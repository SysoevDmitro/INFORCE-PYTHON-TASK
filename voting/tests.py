from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Restaurant, Menu, Vote


class TestLunchVote(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@lunchvote.com", password="adminpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_restaurant_401(self):
        self.client.logout()
        url = reverse('voting:restaurant-list')
        data = {'name': 'Test Restaurant', "address": "Test Address"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_restaurant_201(self):
        url = reverse('voting:restaurant-list')
        data = {'name': 'Test Restaurant', "address": "Test Address"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Restaurant.objects.count(), 1)
        self.assertEqual(Restaurant.objects.get().name, 'Test Restaurant')

    def test_create_menu_401(self):
        self.client.logout()
        url = reverse('voting:menu-list')
        restaurant = Restaurant.objects.create(name='Test Restaurant')
        data = {
            'restaurant': restaurant.id,
            'date': '2024-08-14',
            'items': 'Pizza, Salad, Soup'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu_201(self):
        url = reverse('voting:menu-list')
        restaurant = Restaurant.objects.create(name='Test Restaurant', address='Test Address')
        data = {
            'restaurant': restaurant.id,
            'date': '2024-08-14',
            'description': 'Pizza, Salad, Soup'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)
        self.assertEqual(Menu.objects.get().description, 'Pizza, Salad, Soup')

    def test_create_vote(self):
        url = reverse('voting:vote-list')


class TestVote(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@lunchvote.com", password="adminpass"
        )
        self.client.force_authenticate(user=self.user)
        self.restaurant = Restaurant.objects.create(name="Restaurant", address="Address")
        self.menu = Menu.objects.create(restaurant=self.restaurant,
                                        description="Salad, fish",
                                        date="2024-08-14")

    def test_vote_201(self):
        self.client.logout()
        url = reverse('voting:vote-list')
        data = {'menu': self.menu.id, "user": self.user.id, "date": "2024-08-14"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_vote_twice_same_day(self):
        url = reverse('voting:vote-list')
        data = {'menu': self.menu.id, "user": self.user.id, "date": "2024-08-14"}
        # First vote
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

        # Second vote on the same day
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vote.objects.count(), 1)

    def test_vote_different_days(self):
        url = reverse('voting:vote-list')
        data = {'menu': self.menu.id, "user": self.user.id, "date": "2024-08-14"}
        # First vote
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

        # Create a new menu for a different day
        new_menu = Menu.objects.create(
            restaurant=self.restaurant, date='2024-08-15', description='Burger, Fries'
        )

        # Vote for the new day
        data = {'menu': new_menu.id, "user": self.user.id, "date": "2024-08-15"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 2)
