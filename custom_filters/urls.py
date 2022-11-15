from django.urls import path
from . import views

app_name = 'custom_filters'

urlpatterns = [
    path('users-filtered/<str:letter>', views.LetterUserList.as_view()),
    path('list-author/<str:book>', views.book_author_search_filter),

]