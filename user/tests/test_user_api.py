"""
Test for user api.
"""
from decimal import Decimal
import datetime

from django.utils import timezone, dateformat

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from uljesaKojadinovic.relations import add_days_for_three_months, add_days_to_month
import datetime

CREATE_USER_API = reverse('user:signup')
TOKEN_URL = reverse('token_obtain_pair')

def detail_url(user_id):
    return reverse('user:update-user', args=[user_id])

def create_user(**params):
    """Create and return new user"""
    return get_user_model().objects.create_user(**params)


def payloadWithConfirmPass(arg):

    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': 'three-months',
        'fee': Decimal('30.00'),
        'password': arg,
        'confirm_password': arg,
    }
    return payload


def payloadUser(arg):
    payload = {
        'email': 'user@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': 'three-months',
        'fee': Decimal('30.00'),
        'password': arg,
    }
    return payload


def payloadUserWithOptions(arg, option, fee_num):

    md = ''
    if option == 1:
        md = "one-month"
    elif option == 2:
        md = "three-months"
    elif option == 3:
        md = "half-year"
    elif option == 4:
        md = "one-year"

    payload = {
        'email': 'user1@example.com',
        'first_name': 'Marko',
        'last_name': 'Markovic',
        'phone_number': '+38765222222',
        'membership_duration': md,
        'fee': fee_num,
        'password': arg,
        'confirm_password': arg,
    }

    return payload


class PublicUserApiTest(TestCase):
    """Test the public features of the userAPI"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user successfully"""
        data = payloadWithConfirmPass('test1234$$')
        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=data['email'])


        self.assertEqual(user.email, data['email'])
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.phone_number, data['phone_number'])
        self.assertEqual(user.membership_duration, data['membership_duration'])
        self.assertEqual(user.fee, data['fee'])

        self.assertTrue(user.check_password(data['password']))
        self.assertNotIn('password', res.data)

    def test_if_user_email_exists(self):
        """Test if user with email exists"""
        data = payloadWithConfirmPass('test1234$$')
        create_user(**payloadUser('test1234$$'))
        res = self.client.post(CREATE_USER_API, data)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_if_password_too_short(self):
        """Test to return error if password iz less than 7 char"""
        data = payloadWithConfirmPass('dr567')
        email = data['email']
        res = self.client.post(CREATE_USER_API, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        getUser = get_user_model().objects.filter(
            email=email
        ).exists()
        self.assertFalse(getUser)

    def test_create_jwt_for_user(self):
        """Test for creating jwt for user"""
        payload = payloadUser('testpass123')
        create_user(**payload)
        dataT = {
            'password': payload['password'],
            'email': payload['email']
        }


        token = self.client.post(TOKEN_URL, dataT)
        self.assertIn('access', token.data)
        self.assertEqual(token.status_code, status.HTTP_200_OK)

    def test_bad_credentials_for_jwt(self):
        """Test bad credentials for jwt token"""
        payload = payloadUser('test123123')
        create_user(**payload)
        dataT = {
            'password': 'jdjdjdjdjdjdj',
            'email': payload['email']
        }
        token = self.client.post(TOKEN_URL, dataT)
        self.assertNotIn('access', token.data)
        self.assertEqual(token.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_creat_token_blank_password(self):
        """Test if no password for creating jwt token"""
        payload = payloadUser('test123123')
        create_user(**payload)
        dataT = {
            'password': '',
            'email': payload['email']
        }
        token = self.client.post(TOKEN_URL, dataT)
        self.assertNotIn('access', token.data)
        self.assertEqual(token.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """If user is not authorized"""
        res = self.client.get(detail_url(1), {})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateUserApiTest(TestCase):
    """Test API request that require authentication."""

    def setUp(self) -> None:
        self.user = create_user(**payloadUser('test1234$$'))
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrive_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(detail_url(1))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res_data = {}
        listOfData = ['id', 'date_joined', 'start_date', 'end_date']
        for item in res.data:
            if item not in listOfData:
                res_data[item] = res.data[item]

        self.assertEqual(res_data, {
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'phone_number': self.user.phone_number,
            'membership_duration': self.user.membership_duration,
            'fee': self.user.fee,
            'duration': self.user.duration,
            'is_active': self.user.is_active,
        })

    def test_post_method_not_allowed(self):
        """Test POST method not allowed for endpoint"""
        res = self.client.post(detail_url(1), {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_first_name(self):
        """Test PATCH method for user."""
        update_data = {'first_name': 'Dragan', 'password': 'myNewPassword1234',}

        res = self.client.patch(detail_url(1), update_data)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, update_data['first_name'])
        self.assertTrue(self.user.check_password(update_data['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_if_update_field_on_creating_new_user_one_month(self):
        """Test if save method update fields on creating new user with one month membership"""

        payload = payloadUserWithOptions("test$$1234", 1, "30.00")
        res = self.client.post(CREATE_USER_API, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.membership_duration, payload["membership_duration"])

        days = add_days_to_month()
        start_day_now = datetime.date.today()
        end_date = datetime.date.today() + datetime.timedelta(days=days)
        self.assertEqual(user.start_date, start_day_now)
        self.assertEqual(user.end_date, end_date)
        self.assertEqual(user.duration, days)
        self.assertEqual(user.active_member, True)

    def test_if_update_field_on_creating_new_user_three_month(self):
        """Test if save method update fields on creating new user with three month membership"""

        payload = payloadUserWithOptions("test$$1234", 2, "30.00")
        res = self.client.post(CREATE_USER_API, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.membership_duration, payload["membership_duration"])

        days_of_three_months = add_days_for_three_months(payload["membership_duration"])
        start_day_now = datetime.date.today()
        end_date = datetime.date.today() + datetime.timedelta(days=days_of_three_months)
        self.assertEqual(user.start_date, start_day_now)
        self.assertEqual(user.end_date, end_date)
        self.assertEqual(user.duration, days_of_three_months)
        self.assertEqual(user.active_member, True)

    def test_if_update_field_on_creating_new_user_half_year(self):
        """Test if save method update fields on creating new user with half year membership"""

        payload = payloadUserWithOptions("test$$1234", 3, "30.00")
        res = self.client.post(CREATE_USER_API, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.membership_duration, payload["membership_duration"])

        days_of_three_months = add_days_for_three_months(payload["membership_duration"])
        start_day_now = datetime.date.today()
        end_date = datetime.date.today() + datetime.timedelta(days=days_of_three_months)
        self.assertEqual(user.start_date, start_day_now)
        self.assertEqual(user.end_date, end_date)
        self.assertEqual(user.duration, days_of_three_months)
        self.assertEqual(user.active_member, True)

    def test_if_update_field_on_creating_new_user_one_year(self):
        """Test if save method update fields on creating new user with one year membership"""

        payload = payloadUserWithOptions("test$$1234", 4, "30.00")
        res = self.client.post(CREATE_USER_API, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.membership_duration, payload["membership_duration"])

        days_of_three_months = add_days_for_three_months(payload["membership_duration"])
        start_day_now = datetime.date.today()
        end_date = datetime.date.today() + datetime.timedelta(days=days_of_three_months)
        self.assertEqual(user.start_date, start_day_now)
        self.assertEqual(user.end_date, end_date)
        self.assertEqual(user.duration, days_of_three_months)
        self.assertEqual(user.active_member, True)

    def test_if_creating_user_fee_is_zero(self):
        """Test if save method update active_member on 0.00 fee equals false"""

        payload = payloadUserWithOptions("test$$1234", 4, "0.00")
        res = self.client.post(CREATE_USER_API, payload)
        user = get_user_model().objects.get(email=payload["email"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, payload["email"])
        self.assertEqual(user.membership_duration, '')
        self.assertEqual(user.active_member, False)




























