from celery import Celery, shared_task
from .models import AuthorBook, BorrowBook, LibraryUser
from django.core.mail import send_mail
@shared_task
def create_new_author(data):
    dataFromAdmin = data
    firstName = dataFromAdmin['first_name']
    lastName = dataFromAdmin['last_name']
    year_of_birth = dataFromAdmin['year_of_birth']
    AuthorBook.objects.create(first_name=firstName, last_name=lastName, year_of_birth=year_of_birth)
    print('in tasks', firstName, lastName)
    return f'You created new author {firstName} {lastName}'

@shared_task(bind=True)
def return_book_duration(self):
    returning_due = BorrowBook.objects.filter(returned=False)
    email = LibraryUser.objects.get(email='bogosavacm@yahoo.com')
    print('ovde sam u schedule')
    for ret in returning_due:
        counter = ret.days_left
        print(counter)
        print(ret.borrower.email)
        ret.save()
        if counter == 1:
            book = ret.book
            senderEmail = email.email
            subject = 'Announcement for returning book'
            message = f'Your due to return book {book} to library is tomorrow!'
            recieverEmail = ret.borrower.email
            send_mail(subject, message, 'realauto.polovniautomobili@gmail.com', [recieverEmail], fail_silently=False)
        elif counter - 1 == -1:
            book = ret.book
            senderEmail = email.email
            subject = 'Announcement for returning book'
            message = f'Your due to return book {book} to library is today!'
            recieverEmail = ret.borrower.email
            send_mail(subject, message, 'realauto.polovniautomobili@gmail.com', [recieverEmail], fail_silently=False)
        elif counter - 1 < -1:
            book = ret.book
            senderEmail = email.email
            subject = 'Announcement for returning book'
            message = f'Your due to return book {book} expired!'
            recieverEmail = ret.borrower.email
            send_mail(subject, message, 'realauto.polovniautomobili@gmail.com', [recieverEmail], fail_silently=False)
    return 'done'

@shared_task(bind=True)
def membership_days_left(self):
    queryset = LibraryUser.objects.all()
    for user in queryset:
        if user.active_member == True and user.days_left > -1:
            user.save()
        elif user.days_left < 0:
            user.active_member = False
            user.membership_duration = ''
            user.fee = '0.00'
    return 'Done'





