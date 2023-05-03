from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.test import TestCase
from user.models import User

from tests.constants import (TEST_EMAIL, TEST_FIRST_NAME, TEST_LAST_NAME,
                             TEST_PASSW, API_REGISTER_URL, API_LOGIN_URL,
                             TEST_EMAIL2)


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            password=TEST_PASSW
        )

    def test_if_user_was_created_with_complete_credentials(self):
        self.assertTrue(User.objects.filter(
            email=TEST_EMAIL).exists())

    def test_if_user_can_be_created_without_email(self):
        self.assertTrue(User.objects.create(
            email="", password=TEST_PASSW))

    def test_if_user_can_be_created_without_password(self):
        self.assertTrue(User.objects.create(
            email=TEST_EMAIL2, password=""))

    def tests_if_user_can_be_created_with_invalid_email(self):
        self.assertTrue(User.objects.create(
            email="test_user.com", password=TEST_PASSW))

    def tests_if_user_can_be_created_with_1_character_password(self):
        self.assertTrue(User.objects.create(
            email='test_user_email3@test.com', password="a"))

    def tests_if_it_is_possible_to_update_the_users_first_name(self):
        self.assertTrue(User.objects.filter(
            email=TEST_EMAIL).update(first_name=TEST_FIRST_NAME))

    def tests_if_it_is_possible_to_update_the_users_last_name(self):
        self.assertTrue(User.objects.filter(
            email=TEST_EMAIL).update(last_name=TEST_FIRST_NAME))

    def test_if_user_is_staff(self):
        self.assertFalse(self.user.is_staff)

    def test_if_user_is_superuser(self):
        self.assertFalse(self.user.is_superuser)

    def test_if_user_can_authenticate_with_correct_credentials(self):
        user = User.objects.get(email=TEST_EMAIL)
        self.assertTrue(user.check_password(TEST_PASSW))


class RegisterUserViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_with_valid_data(self):
        data = {
            "first_name": TEST_FIRST_NAME,
            "last_name": TEST_LAST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSW,
            "password_confirm": TEST_PASSW
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_register_user_with_invalid_data(self):

        data = {
            "first_name": TEST_FIRST_NAME,
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
            "last_name": TEST_LAST_NAME,
            "email": TEST_EMAIL,
            "password": TEST_PASSW
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_invalid_last_name(self):

        data = {
            "first_name": TEST_FIRST_NAME,
            "last_name": "ASDASD21d 112 d1@ dsa",
            "email": TEST_EMAIL,
            "password": TEST_PASSW
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_without_password(self):

        data = {
            "first_name": TEST_FIRST_NAME,
            "last_name": TEST_LAST_NAME,
            "email": TEST_EMAIL,
            "password": ""
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_short_numeric_password(self):

        data = {
            "first_name": TEST_FIRST_NAME,
            "last_name": TEST_LAST_NAME,
            "email": TEST_EMAIL,
            "password": "13"
        }
        response = self.client.post(API_REGISTER_URL, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)


class LoginUserAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            password=TEST_PASSW
        )

    def test_login_user_with_valid_credentials(self):
        url = API_LOGIN_URL
        data = {
            'email': TEST_EMAIL,
            'password': TEST_PASSW
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data[0])

    def test_login_user_with_invalid_credentials(self):
        url = API_LOGIN_URL
        data = {
            'email': TEST_EMAIL,
            'password': 'invalidhublapassword'
        }
        response = self.client.post(url, data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'Please check your credentials!')

    def test_login_user_with_missing_email(self):
        url = API_LOGIN_URL
        data = {
            'password': 'invalidhublapassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'Please check your credentials!')

    def test_login_user_with_missing_password(self):
        url = API_LOGIN_URL
        data = {
            'email': TEST_EMAIL
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'],
                         'Please check your credentials!')
