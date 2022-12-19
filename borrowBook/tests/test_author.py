"""
Test for author API
"""

import datetime
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
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


class CreatePublicAuthorApiTest(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test if no authentication"""
        res = self.client.get(AUTHOR_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateAuthorApiTest(TestCase):
    """Test create, list, detail, update author, book and book borrow models"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.data = payloadUser("test$$1234")
        self.user = create_user(**self.data)
        self.user.refresh_from_db()
        self.access_token = self.client.post(
            TOKEN_URL,{
                "password": self.data['password'],
                "email": self.data["email"]
            }
        ).data.get("access")
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_superuser_successfully(self):
        """Create superuser for author tests"""
        user = self.client.get(detail_url(1), )
        self.assertEqual(user.status_code, status.HTTP_200_OK)

    def test_retrieve_author(self):
        """Test retrieving a list of authors"""
        create_author()
        create_author()

        res = self.client.get(AUTHOR_URL)
        author = AuthorBook.objects.all()
        serializer = AuthorBookSerializer(author, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        print(res.data)
        print(serializer.data)
        self.assertEqual(res.data, serializer.data)


    def test_get_author_detail(self):
        """Test get author detail"""
        author = create_author()

        url = author_detail_url(author.id)
        res = self.client.get(url)

        serializer = AuthorBookSerializer(author)
        self.assertEqual(res.data, serializer.data)


    def test_create_new_author(self):
        """Test to create new author in db"""
        AuthorBook.objects.create(first_name="Dragan", last_name="Draganovic", year_of_birth="1966-07-14")
        AuthorBook.objects.create(first_name="Milan", last_name="Milanovic", year_of_birth="1977-07-18")

        res = self.client.get(AUTHOR_URL)

        authors = AuthorBook.objects.all().order_by("last_name")
        serializer = AuthorBookSerializer(authors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_author(self):
        """Update author object in db"""
        new_author = AuthorBook.objects.create(first_name="Dragan", last_name="Draganovic", year_of_birth="1966-07-14")
        url = author_detail_url(new_author.id)
        payload = {"first_name": "Milan"}
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_author.refresh_from_db()
        self.assertEqual(new_author.first_name, payload["first_name"])

    def test_full_update_author(self):
        """Full update author object in db"""
        new_author = AuthorBook.objects.create(first_name="Draga", last_name="Draganovi", year_of_birth="1966-07-14")
        url = author_detail_url(new_author.id)
        payload = {
            "first_name": "Dragan",
            "last_name": "Draganovic",
            "year_of_birth": "1966-07-13"
        }

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_author.refresh_from_db()
        for k, v in payload.items():
            if k == 'year_of_birth':
                date = datetime.datetime.strftime(getattr(new_author, k), "%Y-%m-%d")
                self.assertEqual(date, v)
            else:
                self.assertEqual(getattr(new_author, k), v)


    def test_delete_author(self):
        """Delete author from database"""

        payload = {
            "first_name": "Dragan",
            "last_name": "Draganovic",
            "year_of_birth": "1966-07-13",
        }
        new_author = self.client.post(AUTHOR_URL, payload)
        author = AuthorBook.objects.get(id=1)

        self.assertEqual(new_author.status_code, status.HTTP_201_CREATED)
        res = self.client.delete(author_detail_url(author.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        auth = AuthorBook.objects.filter(id=author.id).exists()
        self.assertFalse(auth)


    def test_create_new_book(self):
        """Test to create new book in db"""
        author1 = AuthorBook.objects.create(first_name="Dragan", last_name="Draganovic", year_of_birth="1966-07-14")
        author2 = AuthorBook.objects.create(first_name="Mirko", last_name="Mirkovic", year_of_birth="1945-08-22")

        payload = {
            "book_name": 'New book',
            "release_year": datetime.datetime(1985, 10, 20),
            "pages": 300,
            "ganres": "Health & Fitness",
            "quantity": 100,
            "in_stock": 100,
            "author": [{"id": author1.id, }]
        }










