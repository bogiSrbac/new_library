"""
URL mapping for borrow the book
"""
import pprint
from django.urls import path, include, re_path

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter(trailing_slash=False)
router.register('borrow-book-new', views.BorrowBookViewSet)
router.register('author', views.AuthorBookDetailUpdateDestroyAPIView)

app_name = 'borrowBook'

urlpatterns = [
    path('', include(router.urls))
]
