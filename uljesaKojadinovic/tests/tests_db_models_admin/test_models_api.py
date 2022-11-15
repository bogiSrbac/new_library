"""
Tests for models
"""
from decimal import Decimal
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from datetime import datetime
from uljesaKojadinovic import models


def payload_with_confirm_pass(arg):
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


def payload_user(email, arg):
    payload = {
        'email': email,
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': 'three-months',
        'fee': Decimal('30.00'),
        'password': arg,
    }
    return payload


def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


class TestModels(TestCase):

    def test_create_user_with_email_successful(self):
        """Test create user with email"""
        user_data = payload_user('user@example.com', 'test1234pass')
        email = user_data['email']
        password = user_data['password']

        user = create_user(**user_data)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_emil_normalized(self):
        """Test if email is normalized"""

        emails = [
            ['user1@EXAMPLE.com', 'user1@example.com'],
            ['User2@Example.com', 'User2@example.com'],
            ['USER3@EXAMPLE.COM', 'USER3@example.com'],
            ['user4@EXAMPLE.COM', 'user4@example.com'],
        ]

        for email, expected in emails:
            user_data = payload_user(email, 'test123pass')
            user = create_user(**user_data)
            self.assertEqual(user.email, expected)

    def test_no_provided_email_error(self):
        """Test create user without email error"""

        with self.assertRaises(ValueError):
            data = payload_user('', 'test123pass')
            create_user(**data)

    def test_create_superuser(self):
        """Test create superuser"""

        user_data = payload_user('user@example.com', 'test123pass')
        user = get_user_model().objects.create_superuser(**user_data)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


    def test_create_author(self):
        """Test create author """
        date = datetime.strptime('1954-8-12', '%Y-%m-%d')
        author = models.AuthorBook.objects.create(
            first_name='Branko',
            last_name='Copic',
            year_of_birth=date
        )

        self.assertEqual(str(author), author.last_name + ' ' + author.first_name)

    def test_create_book(self):
        """Test create book is successful"""
        date = datetime.strptime('1954-8-12', '%Y-%m-%d')
        author = models.AuthorBook.objects.create(first_name='Branko', last_name='Copic', year_of_birth=date)
        author1 = models.AuthorBook.objects.create(first_name='Ivo', last_name='Andric', year_of_birth=date)

        list_of_authors = [author, author1]

        book = models.Book.objects.create(
            book_name='Na Drini cuprija',
            release_year=date,
            pages=255,
            ganres='Technology',
            quantity=120,
            in_stock=120
        )
        book.author.add(author, author1)

        self.assertEqual(str(book), book.book_name)
        for b in book.author.all():
            self.assertIn(b, list_of_authors)


    def test_create_borrow_book(self):
        """Test creating borrow book is successful"""
        payload = payload_user('user@example.com', 'test1234pass')
        user = create_user(**payload)

        date = datetime.strptime('1954-8-12', '%Y-%m-%d')
        author = models.AuthorBook.objects.create(first_name='Branko', last_name='Copic', year_of_birth=date)
        author1 = models.AuthorBook.objects.create(first_name='Ivo', last_name='Andric', year_of_birth=date)

        book = models.Book.objects.create(
            book_name='Na Drini cuprija',
            release_year=date,
            pages=255,
            ganres='Technology',
            quantity=120,
            in_stock=120
        )
        book.author.add(author, author1)

        borrow_book = models.BorrowBook.objects.create(
            borrower=user,
            book=book,
        )

        self.assertEqual(str(borrow_book), str(borrow_book.book.book_name) + ' ' + str(borrow_book.borrower.last_name)
                         + ' ' + str(borrow_book.borrower.first_name))



























