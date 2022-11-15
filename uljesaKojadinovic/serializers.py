from rest_framework import serializers
from .models import LibraryUser, Book, AuthorBook, BorrowBook
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework.validators import UniqueTogetherValidator
import datetime
from rest_framework.settings import api_settings


class CreateAuthorSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150, allow_null=True)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150, allow_null=True)
    year_of_birth = serializers.DateField()

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=AuthorBook.objects.all(),
                fields=['first_name', 'last_name', 'year_of_birth']
            )
        ]

    def create(self, validated_data):
        return AuthorBook.objects.create(**validated_data)







class BooksToAuthorSerialzer(serializers.ModelSerializer):
    """Serializer to set books to authors"""
    class Meta:
        model = Book
        fields = ['id', 'book_name', 'release_year', 'pages', 'ganres', 'author', 'quantity', 'in_stock', 'author']
        read_only_fields = ['id']

class AuthorBookSerializer(serializers.ModelSerializer):
    books = BooksToAuthorSerialzer(many=True, required=False)

    class Meta:
        model = AuthorBook
        fields = ['id', "first_name", "last_name", "year_of_birth", 'books']

    def get_books(self, obj):
        products = Book.objects.filter(author=obj)  # will return product query set associate with this category
        response = BookSerializer(products, many=True).data
        return response

    def _get_or_create_books(self, books, authors):
        """Handle getting or creating authors as needed."""
        for book in books:
            book_object, created = Book.objects.get_or_create(
                **book
            )
            authors.book.add(book_object)

    def create(self, validated_data):
        """Create a author"""
        books = validated_data.pop('book', [])
        author = AuthorBook.objects.create(**validated_data)
        self._get_or_create_books(books, author)
        return author

    def update(self, instance, validated_data):
        """Update authors"""
        book = validated_data.pop('book', None)
        if book is not None:
            instance.book.clear()
            self._get_or_create_books(book, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class BookSerializer(serializers.ModelSerializer):
    author2 = AuthorBookSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'book_name', 'release_year', 'pages', 'ganres', 'author', 'quantity', 'in_stock', 'author2']


class BorrowBookSerilaizer(serializers.ModelSerializer):
    # lend_date = serializers.ReadOnlyField()
    # return_date = serializers.ReadOnlyField()
    duration = serializers.ReadOnlyField()
    days_left = serializers.ReadOnlyField()

    class Meta:
        model = BorrowBook
        fields = ['id', 'borrower', 'book', 'lend_date', 'return_date', 'duration', 'days_left', 'returned']

    def validate(self, attrs):
        queryset = BorrowBook.objects.filter(borrower=attrs['borrower'], returned=False)
        querysetBook = BorrowBook.objects.filter(borrower=attrs['borrower'], borrower__borrowbook__book=attrs['book'])
        queryset = len(list(queryset))
        bookName = attrs['book']
        in_stock = Book.objects.get(book_name=bookName.book_name)
        if queryset >= 3 and self.context.get('request').method != "PUT":
            raise serializers.ValidationError("On your account you already have 3 book borrowed")
        elif querysetBook and self.context.get('request').method != "PUT":
            raise serializers.ValidationError(f"You already borrowed book {attrs['book']}")
        elif in_stock.in_stock <= 0:
            raise serializers.ValidationError(f"You have no book {attrs['book']} in stock")
        return attrs


class GlobalSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorBook
        fields = '__all__'

        def to_native(self, obj):
            if isinstance(obj, Book):
                serializer = BookSerializer(obj)
            elif isinstance(obj, AuthorBook):
                serializer = AuthorBookSerializer(obj)
            else:
                raise Exception("Neither a Book nor Author instance!")
            return serializer.data
