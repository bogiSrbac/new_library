from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions, authentication, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import LibraryUser, Book, AuthorBook, BorrowBook
from .serializers import (BookSerializer, CreateAuthorSerializer, GlobalSearchSerializer,
                          AuthorBookSerializer, BorrowBookSerilaizer,)
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth import authenticate, logout
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, permission_classes, action
from .tasks import create_new_author
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models import Q
from itertools import chain
# @receiver(post_save, sender=LibraryUser)



def base_html(request):
    return render(request, 'uljesaKojadinovic/base.html')


def index(request):
    return render(request, 'uljesaKojadinovic/index.html')

def room(request, room_name):
    return render(request, 'uljesaKojadinovic/room.html', {
        'room_name': room_name
    })


def userPreSave(sender, instance, *args, **kwargs):
    if instance.id is None:
        pass
    else:
        query = LibraryUser.objects.filter(email=instance.email).values("email", "first_name", "last_name", "phone_number",
                                                                        "membership_duration", "start_date", "end_date",
                                                                        "fee", "duration", "active_member")

        data = list(query)
        listOfInstancesValues = [instance.email, instance.first_name, instance.last_name, instance.phone_number,
                                 instance.membership_duration, instance.start_date, instance.end_date,
                                 instance.fee, instance.duration, instance.active_member]
        listOfInstances = {}
        changed_data = {}
        counter = 0
        for i in data[0]:
            listOfInstances[i] = listOfInstancesValues[counter]
            counter = counter + 1
        for key in data[0]:
            if data[0][key] != listOfInstances[key]:
                 print(key, data[0][key], listOfInstances[key])
                 changed_data[key] = f"previous: {data[0][key]}, after update {listOfInstances[key]}"

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            'chat_momir',
            {
                'type': 'chat.message',
                'message': changed_data,
            }
        )

pre_save.connect(userPreSave, sender=LibraryUser)



class AuthorBookListAPIView(generics.ListAPIView):
    queryset = AuthorBook.objects.all()
    serializer_class = AuthorBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]



    # def get_queryset(self):
    #     if self.kwargs['books']:
    #         book_or_author_name = self.kwargs["books"]
    #         querysetAuthor = AuthorBook.objects.filter(Q(last_name__startswith=book_or_author_name) |
    #                                              Q(first_name__startswith=book_or_author_name))
    #         querysetBook = Book.objects.filter(book_name__startswith=book_or_author_name)
    #         queryset = list(chain(querysetAuthor, querysetBook))
    #         print(queryset)
    #         return queryset






class AuthorBookCreateAPIView(generics.ListCreateAPIView):
    queryset = AuthorBook.objects.all()
    serializer_class = AuthorBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [authentication.TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save()


class AuthorBookDetailUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AuthorBook.objects.all()
    serializer_class = AuthorBookSerializer
    permission_classes = [permissions.IsAdminUser]


class BookListAPIView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookCreateAPIView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()

class BookDetailUpdateDestoyAPIViwe(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]

class BorrowerBookListAPIView(generics.ListAPIView):
    queryset = BorrowBook.objects.all()
    serializer_class = BorrowBookSerilaizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BorrowerBookListCreateAPIView(generics.ListCreateAPIView):
    queryset = BorrowBook.objects.all()
    serializer_class = BorrowBookSerilaizer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class BorrowerBookDetailUpdateDestoyAPIViwe(generics.RetrieveUpdateDestroyAPIView):
    queryset = BorrowBook.objects.all()
    serializer_class = BorrowBookSerilaizer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]













@api_view(["GET", "POST"])
@permission_classes([])
def create_author(request):
    if request.method == "POST":

        serializer = CreateAuthorSerializer(data=request.data)

        if serializer.is_valid():
            create_new_author.delay(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message':'Author successfully created'})


from django.core.mail import send_mail


@csrf_exempt
def frak(request):
    hdhdd = LibraryUser.objects.get(email='bogosavacm@yahoo.com')
    send_mail('test poruka', 'Samo provjera', 'realauto.polovniautomobili@gmail.com', ['realauto.polovniautomobili@gmail.com'], fail_silently=False)
    if request.method == "GET":
        query = BorrowBook.objects.filter(returned=False)
        for q in query:
            print(q.borrower.email)
        return Response({'message':"jkdjejkw"})
    return Http404

