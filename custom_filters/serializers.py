"""
Serializers for user, book and author filter
"""
from rest_framework import serializers
from uljesaKojadinovic.models import LibraryUser, Book, AuthorBook


class LibraryUserSerializer(serializers.ModelSerializer):
    # end_date = serializers.ReadOnlyField()
    # duration = serializers.ReadOnlyField()
    # active_member = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    id = serializers.ReadOnlyField()

    class Meta:
        model = LibraryUser
        fields = ['id', 'first_name', 'last_name', 'phone_number',
                  'membership_duration', 'fee',
                  'email', 'password', ]


class AuthorBookSerializerFilter(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()

    class Meta:
        model = AuthorBook
        fields = ['id', "first_name", "last_name", "year_of_birth", 'books']

    def get_books(self, obj):
        products = Book.objects.filter(author=obj)  # will return product query set associate with this category
        response = BookSerializerFilter(products, many=True).data
        print(obj)
        return response

class BookSerializerFilter(serializers.ModelSerializer):
    author2 = AuthorBookSerializerFilter(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'book_name', 'release_year', 'pages', 'ganres', 'author', 'quantity', 'in_stock', 'author2']