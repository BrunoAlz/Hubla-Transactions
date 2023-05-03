from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase, Client
from django.test import TestCase
from user.models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test_user_email@test.com",
            password="testpassword"
        )

    def test_if_user_was_created_with_complete_credentials(self):
        self.assertTrue(User.objects.filter(
            email='test_user_email@test.com').exists())

    def test_if_user_can_be_created_without_email(self):
        self.assertTrue(User.objects.create(
            email="", password="testpassword"))

    def test_if_user_can_be_created_without_password(self):
        self.assertTrue(User.objects.create(
            email="test_user_email2@test.com", password=""))

    def tests_if_user_can_be_created_with_invalid_email(self):
        self.assertTrue(User.objects.create(
            email="test_user.com", password='testpassword'))

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
        self.assertTrue(user.check_password('testpassword'))


class RegisterUserViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user_with_valid_data(self):

        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "mypassword"
        }
        response = self.client.post(
            "/api/users/register/", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
