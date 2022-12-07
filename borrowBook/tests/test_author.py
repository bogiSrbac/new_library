"""
Test for author API
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_API = reverse('user:signup')
TOKEN_URL = reverse('token_obtain_pair')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

def payloadWithConfirmPass(arg):
    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': 'three-months',
        'fee': Decimal('30.00'),
        'password': arg,
        'confirm_password': arg,
    }
    return payload


def payloadUser(arg):
    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': 'three-months',
        'fee': Decimal('30.00'),
        'password': arg,
    }
    return payload


class CreateAuthorApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def create_superuser_successfully(self):
        """Create suepr user for author tests"""
        data = payloadWithConfirmPass('test$$1234')
        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data['email'])

        self.assertEqual(user.emaul, data['email'])