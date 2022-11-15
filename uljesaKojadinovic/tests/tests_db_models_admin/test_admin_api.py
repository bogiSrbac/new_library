"""
Test admin modifications
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal
class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='user@example.com',
            password='testpass123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='user1@example.com',
            first_name='Momir',
            last_name='Bogosavac',
            phone_number='+38765222222',
            membership_duration='three-months',
            fee=Decimal('30.00'),
            password='testpass123', )


    def test_users_list(self):
        """Test users list"""

        url = reverse('admin:uljesaKojadinovic_libraryuser_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.membership_duration)
        self.assertContains(res, self.user.phone_number)
        self.assertContains(res, self.user.fee)

    def test_edit_user_page(self):
        """Test edit user page"""

        url = reverse('admin:uljesaKojadinovic_libraryuser_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page"""

        url = reverse('admin:uljesaKojadinovic_libraryuser_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
























