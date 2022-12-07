# views for borrow book model

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, authentication, generics
import json
from uljesaKojadinovic.models import BorrowBook, AuthorBook, Book, LibraryUser
from . import serializers


class AuthorBookDetailUpdateDestroyAPIView(viewsets.ModelViewSet):
    queryset = AuthorBook.objects.all()
    serializer_class = serializers.AuthorBookSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'put', 'patch', 'delete', 'get']


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BooksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BooksSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class BookDetailUpdateDestoyAPIViwe(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = serializers.BooksSerializer
    permission_classes = [permissions.IsAdminUser]

class BorrowBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowBook.objects.all()
    serializer_class = serializers.BorrowBookSerilaizer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['post', 'put', 'patch', 'delete', 'get']

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



