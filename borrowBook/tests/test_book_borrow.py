"""
Test to create new istance of borrow book
"""

from django.test import TestCase
from uljesaKojadinovic.models import BorrowBook
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


