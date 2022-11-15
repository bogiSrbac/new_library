"""
Custom filters to search users, books and authors
"""

from rest_framework import generics, authentication, permissions
from uljesaKojadinovic.models import AuthorBook, LibraryUser, Book
from . import serializers
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from django.db.models import Q
from itertools import chain


# returning data for users by letter request form
class LetterUserList(generics.ListAPIView):
    serializer_class = serializers.LibraryUserSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if self.kwargs['letter']:
            letter = self.kwargs['letter']
            return LibraryUser.objects.filter(last_name__istartswith=letter).order_by('-last_name', '-first_name')
        elif self.kwargs['id']:
            userId = self.kwargs['id']
            return LibraryUser.objects.get(id=userId)
        elif self.kwargs['search']:
            user = self.kwargs['search']
            users = LibraryUser.objects.filter(last_name__istartswith=user).values('id', 'last_name', 'first_name')
            return users

@api_view(["GET", "POST"])
@permission_classes([])
def book_author_search_filter(request, book):
    if request.method == "GET":

        try:
            searchData = {}
            querysetAuthor = AuthorBook.objects.filter(Q(last_name__startswith=book) |
                                                       Q(first_name__startswith=book))
            if querysetAuthor:
                serializer1 = serializers.AuthorBookSerializerFilter(querysetAuthor, many=True)
                searchData['authors'] = serializer1.data

            querysetBook = Book.objects.filter(book_name__startswith=book)

            if querysetBook:
                serializer2 = serializers.BookSerializerFilter(querysetBook, many=True)
                searchData['books'] = serializer2.data
            return Response(searchData)


        except:
            return Response({'error':'data not find'})
