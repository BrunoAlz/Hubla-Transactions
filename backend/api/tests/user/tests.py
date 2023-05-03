from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from user.models import User
from rest_framework.test import APITestCase


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test_user_email@test.com",
            password="hublapassword"
        )

    def test_if_user_was_created_with_complete_credentials(self):
        self.assertTrue(User.objects.filter(
            email='test_user_email@test.com').exists())

    def test_if_user_can_be_created_without_email(self):
        self.assertTrue(User.objects.create(
            email="", password="hublapassword"))

    def test_if_user_can_be_created_without_password(self):
        self.assertTrue(User.objects.create(
            email="test_user_email2@test.com", password=""))

    def tests_if_user_can_be_created_with_invalid_email(self):
        self.assertTrue(User.objects.create(
            email="test_user.com", password='hublapassword'))

    def tests_if_user_can_be_created_with_1_character_password(self):
        self.assertTrue(User.objects.create(
            email='test_user_email3@test.com', password="a"))

    def tests_if_it_is_possible_to_update_the_users_first_name(self):
        self.assertTrue(User.objects.filter(
            email='test_user_email@test.com').update(first_name='hubla'))

    def tests_if_it_is_possible_to_update_the_users_last_name(self):
        self.assertTrue(User.objects.filter(
            email='test_user_email@test.com').update(last_name='hubla'))

    def test_if_user_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_if_user_is_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_if_user_can_authenticate_with_correct_credentials(self):
        user = User.objects.get(email='test_user_email@test.com')
        self.assertTrue(user.check_password('hublapassword'))


API_REGISTER_URL = "/api/users/register/"


class RegisterUserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_with_valid_data(self):
        data = {
            "first_name": "Hubla",
            "last_name": "Transactions",
            "email": "HublaTransactions@gmail.com",
            "password": "Hubla123@",
            "password_confirm": "Hubla123@"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_with_invalid_data(self):

        data = {
            "first_name": "Hubla",
            "last_name": "1nvalid N4me",
            "email": "invalid-email",
            "password": "1"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_invalid_first_name(self):

        data = {
            "first_name": "d21d12d1d12d1xxx 2 1@ ffw",
            "last_name": "transactions",
            "email": "Hublatransactions@hubla.com",
            "password": "hublapassword"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_invalid_last_name(self):

        data = {
            "first_name": "Hubla",
            "last_name": "ASDASD21d 112 d1@ dsa",
            "email": "Hublatransactions@hubla.com",
            "password": "hublapassword"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_without_password(self):

        data = {
            "first_name": "Hubla",
            "last_name": "transactions",
            "email": "Hublatransactions@hubla.com",
            "password": ""
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_short_numeric_password(self):

        data = {
            "first_name": "Hubla",
            "last_name": "transactions",
            "email": "Hublatransactions@hubla.com",
            "password": "13"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


API_LOGIN_URL = "/api/users/login/"


class LoginUserAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="HublaTransactions@test.com",
            password="hublapassword"
        )

    def test_login_user_with_valid_credentials(self):
        url = API_LOGIN_URL
        data = {
            'email': 'HublaTransactions@test.com',
            'password': 'hublapassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data[0])

    def test_login_user_with_invalid_credentials(self):
        url = API_LOGIN_URL
        data = {
            'email': 'test_user_email@test.com',
            'password': 'invalidpassword'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'Please check your credentials!')

    def test_login_user_with_missing_fields(self):
        url = API_LOGIN_URL
        data = {
            'email': 'test_user_email@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
