from abc import ABC

from rest_framework import serializers
from uljesaKojadinovic.models import BorrowBook, Book, AuthorBook
from rest_framework.validators import UniqueTogetherValidator


class AuthorBookSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = AuthorBook
        fields = ['id', "first_name", "last_name", "year_of_birth", 'books']

    def get_books(self, obj):
        products = Book.objects.filter(author=obj)
        response = BooksSerializer(products, many=True).data
        print(response)

        return response

class BooksSerializer(serializers.ModelSerializer):
    """Serializer to set books to authors"""
    # author2 = AuthorBookSerializer(many=True, read_only=False)

    class Meta:
        model = Book
        fields = ['id', 'book_name', 'release_year', 'pages', 'ganres', 'author', 'quantity', 'in_stock',]
        read_only_fields = ['id']




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
        queryset_ook = BorrowBook.objects.filter(borrower=attrs['borrower'], borrower__borrowbook__book=attrs['book'])
        queryset = len(list(queryset))
        book_name = attrs['book']
        in_stock = Book.objects.get(book_name=book_name.book_name)
        if queryset >= 3 and self.context.get('request').method != "PUT":
            raise serializers.ValidationError("On your account you already have 3 book borrowed")
        elif queryset_ook and self.context.get('request').method != "PUT":
            raise serializers.ValidationError(f"You already borrowed book {attrs['book']}")
        elif in_stock.in_stock <= 0:
            raise serializers.ValidationError(f"You have no book {attrs['book']} in stock")
        return attrs
