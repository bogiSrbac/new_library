"""
Django admin cutomization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(BaseUserAdmin):

    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'membership_duration', 'phone_number', 'fee',]

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name',
                           'phone_number', 'membership_duration', 'fee', 'duration', 'active_member')}),
        (
           _('Permissions'),
           {
               'fields': (
                   'is_active',
                   'is_staff',
                   'is_superuser',
               )
           }
        ),
        (_('Important dates'), {'fields': ('start_date', 'end_date', )})
    )
    readonly_fields = ['last_login', 'last_update',]
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'is_active',
                'is_staff',
                'is_superuser',
            )
        }),
    )

class MembershipInline(admin.TabularInline):
    model = models.Book.author.through

class AuthorAdmin(admin.ModelAdmin):
    inlines = [MembershipInline, ]

admin.site.register(models.LibraryUser, UserAdmin)
admin.site.register(models.AuthorBook, AuthorAdmin)
admin.site.register(models.Book)
admin.site.register(models.BorrowBook)