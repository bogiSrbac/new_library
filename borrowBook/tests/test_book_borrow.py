"""
Test to create new instance of borrow book
"""

from django.test import TestCase
from uljesaKojadinovic.models import BorrowBook, AuthorBook, Book
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..serializers import BorrowBookSerilaizer, AuthorBookSerializer, BooksSerializer

from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
import datetime

CREATE_USER_API = reverse("user:signup")
TOKEN_URL = reverse("token_obtain_pair")
AUTHOR_URL = reverse("borrowBook:authorbook-list")
BOOK_URL = reverse("borrowBook:book-list")
BORROW_BOOK_URL = reverse("borrowBook:borrowbook-list")

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
        'email': 'user1@example.com',
        'first_name': 'Darko',
        'last_name': 'Darkovic',
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

def borrow_book_payload(borrower, book, lend_date):
    payload = {
        "borrower": borrower,
        "book": book,
        "lend_date": lend_date
    }
    return payload

class CreateBorrowBookApiTests(TestCase):

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

    def test_if_create_new_borrow_book_instance_same_authors(self):
        """Test to create same author validation"""
        borrower_data = payloadWithConfirmPass('test$$1234')
        user = self.client.post(CREATE_USER_API, borrower_data)

        self.assertEqual(user.status_code, status.HTTP_201_CREATED)
        borrower_user = get_user_model().objects.get(email=borrower_data["email"])

        author1 = self.client.post(AUTHOR_URL, author_payload())
        author2 = self.client.post(AUTHOR_URL, author_payload())
        self.assertEqual(author1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(author2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("This author already exists in db!", author2.content.decode())

    def test_if_create_new_borrow_book_instance(self):
        """Test to create new borrow book instance with serializer"""
        borrower_data = payloadWithConfirmPass('test$$1234')
        user = self.client.post(CREATE_USER_API, borrower_data)

        self.assertEqual(user.status_code, status.HTTP_201_CREATED)
        borrower_user = get_user_model().objects.get(email=borrower_data["email"])

        new_book1 = book_payload(book_name="Knjiga 1")

        res1 = self.client.post(BOOK_URL, new_book1, format="json")
        book_1_data = Book.objects.get(book_name="Knjiga 1")

        res = self.client.get(BOOK_URL)
        book1 = Book.objects.all().order_by("book_name")
        serilaizer = BooksSerializer(book1, many=True)
        self.assertEqual(res.data, serilaizer.data)
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)

        payload = {
            "borrower": borrower_user.id,
            "book": book_1_data.id,
            "lend_date": datetime.date.today()
        }
        res_created_book = self.client.post(BORROW_BOOK_URL, payload)
        self.assertEqual(res_created_book.status_code, status.HTTP_201_CREATED)

        borrow_res = self.client.get(BORROW_BOOK_URL)
        borrow_all = BorrowBook.objects.all().order_by("borrower")
        serilaizer1 = BorrowBookSerilaizer(borrow_all, many=True)
        self.assertEqual(borrow_res.data, serilaizer1.data)

    def test_if_model_save_method_calculate_data(self):
        """Test are data properly saved in model"""
        borrower_data = payloadWithConfirmPass('test$$1234')
        user = self.client.post(CREATE_USER_API, borrower_data)
        borrower_user = get_user_model().objects.get(email=borrower_data["email"])
        self.assertEqual(user.status_code, status.HTTP_201_CREATED)

        book = book_payload(book_name="New book")
        book_res = self.client.post(BOOK_URL, book, format="json")
        book_data = Book.objects.get(book_name="New book")
        self.assertEqual(book_res.status_code, status.HTTP_201_CREATED)

        book_lend_date = datetime.date.today()
        return_date = book_lend_date + datetime.timedelta(days=15)
        duration = 15
        days = return_date - datetime.date.today()
        days_left = days.days
        in_stock = book["in_stock"] - 1

        payload = {
            "borrower": borrower_user.id,
            "book": book_data.id,
            "lend_date": book_lend_date
        }
        res_created_book = self.client.post(BORROW_BOOK_URL, payload)
        self.assertEqual(res_created_book.status_code, status.HTTP_201_CREATED)

        borrow_book_data = BorrowBook.objects.get(borrower_id=borrower_user.id, book_id=book_data.id)
        book_data1 = Book.objects.get(book_name="New book")
        book_data1.refresh_from_db()

        self.assertEqual(duration, borrow_book_data.duration)
        self.assertEqual(return_date, borrow_book_data.return_date)
        self.assertEqual(days_left, borrow_book_data.days_left)
        self.assertEqual(book_data1.in_stock, in_stock)



    def test_if_user_has_more_than_three_books(self):
        """Test if user has more than three books"""
        borrower_data = payloadWithConfirmPass('test$$1234')
        user = self.client.post(CREATE_USER_API, borrower_data)

        self.assertEqual(user.status_code, status.HTTP_201_CREATED)
        borrower_user = get_user_model().objects.get(email=borrower_data["email"])


        new_book1 = book_payload(book_name="Knjiga 1")
        new_book2 = book_payload(book_name="Knjiga 2")
        new_book3 = book_payload(book_name="Knjiga 3")
        new_book4 = book_payload(book_name="Knjiga 4")

        res1 = self.client.post(BOOK_URL, new_book1, format="json")
        res2 = self.client.post(BOOK_URL, new_book2, format="json")
        res3 = self.client.post(BOOK_URL, new_book3, format="json")
        res4 = self.client.post(BOOK_URL, new_book4, format="json")

        book_data_1 = Book.objects.get(book_name="Knjiga 1")
        book_data_2 = Book.objects.get(book_name="Knjiga 2")
        book_data_3 = Book.objects.get(book_name="Knjiga 3")
        book_data_4 = Book.objects.get(book_name="Knjiga 4")

        res = self.client.get(BOOK_URL)
        book1 = Book.objects.all().order_by("book_name")
        serilaizer = BooksSerializer(book1, many=True)
        self.assertEqual(res.data, serilaizer.data)

        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res4.status_code, status.HTTP_201_CREATED)

        book_lend_date = datetime.date.today()
        borrower_id = borrower_user.id
        borrow_b_1 = self.client.post(BORROW_BOOK_URL, borrow_book_payload(borrower_id, book_data_1.id, book_lend_date))
        borrow_b_2 = self.client.post(BORROW_BOOK_URL, borrow_book_payload(borrower_id, book_data_2.id, book_lend_date))
        borrow_b_3 = self.client.post(BORROW_BOOK_URL, borrow_book_payload(borrower_id, book_data_3.id, book_lend_date))
        borrow_b_4 = self.client.post(BORROW_BOOK_URL, borrow_book_payload(borrower_id, book_data_4.id, book_lend_date))

        self.assertEqual(borrow_b_1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(borrow_b_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(borrow_b_3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(borrow_b_4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("On your account you already have 3 book borrowed", borrow_b_4.content.decode())



