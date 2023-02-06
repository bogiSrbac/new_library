from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
import datetime
from decimal import Decimal
from .managers import CustomUserManager
from .relations import add_days_to_month, add_days_for_three_months


class LibraryUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    phone_number = PhoneNumberField(_('phone number'), blank=True, null=True)
    PRICE = [
        (Decimal("0.00"), '0.00'),
        (Decimal("10.00"), '10.00'),
        (Decimal("20.00"), '20.00'),
        (Decimal("30.00"), '30.00'),
        (Decimal("40.00"), '40.00'),
        (Decimal("50.00"), '50.00'),
    ]
    MEMBER_DURATION_PERIOD = [
        ('one-month', 'one-month'),
        ('three-months', 'three-months'),
        ('half-year', 'half-year'),
        ('one-year', 'one-year'),
    ]
    membership_duration = models.CharField(_('membership_duration'), max_length=150, blank=True, null=True, choices=MEMBER_DURATION_PERIOD, default='one-year')
    start_date = models.DateField(_('start date'), default=datetime.date.today)
    end_date = models.DateField(_('end date'), blank=True, null=True)
    active_member = models.BooleanField(default=False)
    fee = models.DecimalField(_('fee'), decimal_places=2, max_digits=4, choices=PRICE, default=Decimal("0.00"))
    duration = models.IntegerField(_('duration'), default=0)
    days_left = models.IntegerField(_('days_left'), blank=True, null=True)
    last_update = models.DateField(auto_now=True)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    class Meta:
        get_latest_by = ['last_update']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.fee != 0.00:
            self.active_member = True
            if self.membership_duration == 'one-month':
                days = add_days_to_month()
                self.end_date = self.start_date + datetime.timedelta(days=days)
                self.duration = days
            elif self.membership_duration == 'three-months':
                days_of_three_months = add_days_for_three_months('three-months')
                self.end_date = self.start_date + datetime.timedelta(days=days_of_three_months)
                self.duration = days_of_three_months
            elif self.membership_duration == 'half-year':
                days_of_half_year = add_days_for_three_months('half-year')
                self.end_date = self.start_date + datetime.timedelta(days=days_of_half_year)
                self.duration = days_of_half_year
            elif self.membership_duration == 'one-year':
                days_of_one_year = add_days_for_three_months('one-year')
                self.end_date = self.start_date + datetime.timedelta(days=days_of_one_year)
                self.duration = days_of_one_year
        else:
            self.active_member = False
            self.membership_duration = ''
            self.fee = '0.00'
        super(LibraryUser, self).save(*args, **kwargs)




class AuthorBook(models.Model):
    first_name = models.CharField(_('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    year_of_birth = models.DateField(_('year of birth'), blank=True, null=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return self.last_name + ' ' + self.first_name



class Book(models.Model):
    GANRES = [
        ('Academic & Education', 'Academic & Education'),
        ('Art', 'Art'),
        ('Biography', 'Biography'),
        ('Business & Career', 'Business & Career'),
        ('Environment', 'Environment'),
        ('Fiction & Literature', 'Fiction & Literature'),
        ('Health & Fitness', 'Health & Fitness'),
        ('Lifestyle', 'Lifestyle'),
        ('Personal Growth', 'Personal Growth'),
        ('Politics & Laws', 'Politics & Laws'),
        ('Religion', 'Religion'),
        ('Science & Research', 'Science & Research'),
        ('Technology', 'Technology'),
    ]
    book_name = models.CharField(_('book name'), max_length=150, blank=True, null=True)
    release_year = models.DateField(_('release year'), blank=True, null=True)
    pages = models.IntegerField(_('pages'), default=0)
    ganres = models.CharField(_('ganres'), max_length=150, blank=True, null=True, choices=GANRES)
    author = models.ManyToManyField(AuthorBook, _('author'), blank=True)
    quantity = models.IntegerField(_('quantity'), default=0)
    in_stock = models.IntegerField(_('in_stock'), default=0)

    def __str__(self):
        return self.book_name








class BorrowBook(models.Model):
    borrower = models.ForeignKey(LibraryUser, on_delete=models.CASCADE, blank=True, verbose_name=_('borrower'), default='')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, verbose_name=_('book'), default='')
    lend_date = models.DateField(_('lend date'), default=datetime.date.today)
    return_date = models.DateField(_('return date'), blank=True, null=True)
    duration = models.IntegerField(_('duration'), default=15)
    days_left = models.IntegerField(_('days_left'), default=15)
    returned = models.BooleanField(default=False)

    def __str__(self):
        return str(self.book.book_name) + ' ' + str(self.borrower.last_name) + ' ' + str(self.borrower.first_name)

    def save(self, *args, **kwargs):
        if self.returned is False and self.book.in_stock > 0:
            self.return_date = self.lend_date + datetime.timedelta(days=15)
            self.duration = 15
            days = self.return_date - datetime.date.today()
            self.days_left = days.days
            self.book.in_stock = self.book.in_stock - 1
            self.book.save()
        else:
            self.days_left = 0
            self.duration = 0
            self.book.in_stock = self.book.in_stock + 1
        super(BorrowBook, self).save(*args, **kwargs)






