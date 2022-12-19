"""
Test book api
"""

from decimal import Decimal
import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient
from ..serializers import AuthorBookSerializer, BooksSerializer
from uljesaKojadinovic.models import AuthorBook, Book


CREATE_USER_API = reverse("user:signup")
TOKEN_URL = reverse("token_obtain_pair")
AUTHOR_URL = reverse("borrowBook:authorbook-list")
BOOK_URL = reverse("borrowBook:book-list")


def create_author(**params):
    """Create and return an author"""
    data = {
        "first_name": "Mirko",
        "last_name": "Mirkovic",
        "year_of_birth": "1955-04-25"
    }
    data.update(params)
    author = AuthorBook.objects.create(**data)
    return author


def author_detail_url(id):
    return reverse("borrowBook:authorbook-detail", args=[id])


def book_detail_url(id):
    return reverse("borrowBook:book-detail", args=[id])


def create_user(**params):
    return get_user_model().objects.create_superuser(**params)


def detail_url(user_id):
    return reverse('user:update-user', args=[user_id])


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


def author_payload(first_name="Mirko", last_name="Mirkovic", year_of_birth="1945-03-24"):
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "year_of_birth": year_of_birth
    }
    return payload

def book_payload(book_name="New book", release_year=datetime.datetime.now(),
                 pages=300, ganres="Health & Fitness", quantity=100, in_stock=100, **kwargs):

    payload = {
        "book_name": book_name,
        "release_year": release_year,
        "pages": pages,
        "ganres": ganres,
        "quantity": quantity,
        "in_stock": in_stock,
        **kwargs
    }
    return payload

class CreateBookApiTests(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = payloadUser("test$$1234")
        self.user = create_user(**self.data)
        self.user.refresh_from_db()
        self.access_token = self.client.post(
            TOKEN_URL, {
                "password": self.data['password'],
                "email": self.data["email"]
            }
        ).data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")


    def test_create_superuser_successfully(self):
        """Create superuser for book tests"""
        user = self.client.get(detail_url(1), )
        self.assertEqual(user.status_code, status.HTTP_200_OK)

    def test_retrieve_book(self):
        """Test retrieving list of books"""
        author1 = create_author()
        author2_update = author_payload("Momir", "Momirovic")
        author2 = create_author(**author2_update)
        book = book_payload(authors=[{"id": author1.id}, {"id": author2.id}])
        res = self.client.post(BOOK_URL, book, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


