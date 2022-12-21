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

def create_book(**params):
    """Create and return a book"""
    create_author()
    author2_update = author_payload("Momir", "Momirovic")
    create_author(**author2_update)
    date = '1987-05-20'
    payload = {
        "book_name": "New book",
        "release_year": datetime.date.today(),
        "pages": 100,
        "ganres": "Health & Fitness",
        "quantity": 100,
        "in_stock": 100,
        # "author": [{"id": author1.id}, {"id": author_2.id}]
    }
    payload.update(params)
    book = Book.objects.create(**payload)
    auth = AuthorBook.objects.all()
    book.author.set(auth)
    return book

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

def book_payload(book_name="New book", release_year=datetime.date.today(),
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
        create_book()
        create_book()
        res = self.client.get(BOOK_URL,)
        book = Book.objects.all()
        serializer = BooksSerializer(book, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_book_detail(self):
        """Test book detail"""
        book = create_book()
        res = self.client.get(book_detail_url(book.id))
        serializer = BooksSerializer(book)
        self.assertEqual(res.data, serializer.data)

    def test_create_book_without_author(self):
        """test create book without author instance"""
        # author1 = create_author()
        # author2_update = author_payload("Momir", "Momirovic")
        # author_2 = create_author(**author2_update)
        # author3_update = author_payload("Darko", "Darkic")
        # author_3 = create_author(**author3_update)
        # book_data = book_payload(author=[{"id": author1.id}, {"id": author_2.id}])
        book_data = book_payload()
        res = self.client.post(BOOK_URL, book_data, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        book = Book.objects.get(pk=res.data["id"])
        print(book.author.all(), 'check')
        for k, v in book_data.items():
            self.assertEqual(getattr(book, k), v)

    def test_partial_update_without_author(self):
        """Test partial update of book instance without author"""
        book = create_book()

        payload = {"book_name": 'New book name'}

        res = self.client.patch(book_detail_url(book.id), payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.book_name, payload["book_name"])
        data = book_payload()
        self.assertEqual(book.ganres, data["ganres"])

    def test_full_book_update_without_author(self):
        """Test full book update without author instance"""
        book_original = create_book()

        payload = {
            "book_name": "New book u[dated",
            "release_year": datetime.date.today() + datetime.timedelta(days=1),
            "pages": 200,
            "ganres": "Business & Career",
            "quantity": 200,
            "in_stock": 200,
        }

        url = book_detail_url(book_original.id)
        res = self.client.put(url, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        book_original.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(book_original, k), v)


    def test_delete_book(self):
        """Test deleting a book successfully"""
        book = create_book()

        url = book_detail_url(book.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Book.objects.filter(id=book.id).exists())


    def test_create_book_with_author(self):
        """Test creating a book with new author"""

        author_1 = {
            "first_name": "Mirko",
            "last_name": "Mirkovic",
            "year_of_birth": "1955-04-25"
        }
        author_2 = {
            "first_name": "Darko",
            "last_name": "Darkovic",
            "year_of_birth": "1988-07-05"
        }
        book = {
            "book_name": "New book",
            "release_year": datetime.date.today(),
            "pages": 100,
            "ganres": "Health & Fitness",
            "quantity": 100,
            "in_stock": 100,
            "author": [author_1, author_2]
        }
        res = self.client.post(BOOK_URL, book, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        books = Book.objects.filter(book_name=book['book_name'])
        self.assertEqual(books.count(), 1)
        books = books[0]
        self.assertEqual(books.author.count(), 2)
        for b in book["author"]:
            exists = books.author.filter(
                first_name=b["first_name"],
                last_name=b["last_name"]
            ).exists()
            self.assertTrue(exists)

    def test_Create_book_with_existing_author(self):
        """Test creating book with existing author"""
        author = create_author()
        author_1 = {
            "first_name": "Zarko",
            "last_name": "Zarkovic",
            "year_of_birth": "1955-04-25"
        }
        author_2 = {
            "first_name": "Darko",
            "last_name": "Darkovic",
            "year_of_birth": "1988-07-05"
        }
        book = {
            "book_name": "New book",
            "release_year": datetime.date.today(),
            "pages": 100,
            "ganres": "Health & Fitness",
            "quantity": 100,
            "in_stock": 100,
            "author": [author_1, author_2]
        }

        res = self.client.post(BOOK_URL, book, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        books = Book.objects.filter(book_name=book["book_name"])
        self.assertEqual(books.count(), 1)
        book_db = books[0]
        self.assertEqual(book_db.author.count(), 2)
        self.assertNotIn(author, book_db.author.all())
        for authors in book["author"]:
            exists = book_db.author.filter(
                first_name=authors["first_name"],
                last_name=authors["last_name"]
            ).exists()
            self.assertTrue(exists)







