from django.urls import path
from .views import (create_author, frak, index, room, base_html,
                    AuthorBookCreateAPIView, BookListAPIView, BookCreateAPIView,
                    AuthorBookDetailUpdateDestroyAPIView, BookDetailUpdateDestoyAPIViwe, BorrowerBookDetailUpdateDestoyAPIViwe,
                    BorrowerBookListCreateAPIView, AuthorBookListAPIView, BorrowerBookListAPIView)
from rest_framework.urlpatterns import format_suffix_patterns


app_name = 'uljesaKojadinovic'

urlpatterns = [
    path('', base_html, name='base'),

    path('list-author/', AuthorBookListAPIView.as_view()),
    path('list-create-author/', AuthorBookCreateAPIView.as_view()),
    path('list-create-author/<int:pk>', AuthorBookDetailUpdateDestroyAPIView.as_view()),
    path('create-book/', BookCreateAPIView.as_view()),
    path('list-book/', BookListAPIView.as_view()),
    path('list-create-book/<int:pk>', BookDetailUpdateDestoyAPIViwe.as_view()),
    path('list-borrower-book/', BorrowerBookListAPIView.as_view()),
    path('create-borrower-book/', BorrowerBookListCreateAPIView.as_view()),
    path('create-borrower-book/<int:pk>', BorrowerBookDetailUpdateDestoyAPIViwe.as_view()),

    path('celery/', create_author),
    # path('chat/<str:room_name>/', frak),
    path('channel/', index, name='index'),
    path('channel/<str:room_name>/', room, name='room'),
]



