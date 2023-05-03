from rest_framework.test import APIClient, APITestCase
from user.models import User
from transactions.models import Contract
from user.authentication import JWTAuthentucation
from tests.constants import (TEST_EMAIL, TEST_PASSW, API_CONTRACTS_URL)
from rest_framework import status


class ContractCreateViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_token = None
        self.user_token = self.user = User.objects.create_user(
            email=TEST_EMAIL, password=TEST_PASSW)
        self.token = JWTAuthentucation.generate_jwt(self.user_token.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('TESTANDO CONTRACT CREATION VIEW\n')
        f.close()
        f = open(path, 'rb')
        return {'upload': f}

    def tests_whether_the_creation_of_the_contract_is_correct(self):
        upload = self._create_test_file('sales.txt')
        response = self.client.post(
            API_CONTRACTS_URL, upload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Contract.objects.exists())
        contract = Contract.objects.first()
        self.assertEqual(contract.creator, self.user)
        self.assertEqual(contract.status, '1')
        self.assertEqual(contract.upload.name,
                         'api/uploads/creator/1/sales.txt')

    def Tests_if_the_user_can_access_list_without_contracts(self):
        response = self.client.get(f"{API_CONTRACTS_URL}list/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def tests_contract_listing_for_authenticated_user(self):

        user1 = User.objects.create_user(
            email=f"1{TEST_EMAIL}", password=TEST_PASSW)
        Contract.objects.create(creator=user1, upload='file1.txt', status='1')
        Contract.objects.create(creator=user1, upload='file2.txt', status='2')

        user2 = User.objects.create_user(
            email=f"2{TEST_EMAIL}", password=TEST_PASSW)
        Contract.objects.create(creator=user2, upload='file3.txt', status='1')
        Contract.objects.create(creator=user2, upload='file4.txt', status='2')

        response = self.client.get(f"{API_CONTRACTS_URL}list/")

        contracts = Contract.objects.filter(creator=self.user_token)
        self.assertEqual(len(response.data), len(contracts))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
