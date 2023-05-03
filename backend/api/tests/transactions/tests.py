from django.test import TestCase, Client
from user.models import User
from transactions.models import Contract

from tests.constants import (TEST_EMAIL, TEST_PASSW, API_CONTRACTS_URL)


class ContractCreateViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email=TEST_EMAIL, password=TEST_PASSW)
        self.client.login(username=TEST_EMAIL,
                          password=TEST_PASSW)

    def test_create_contract_successful(self):

        with open('api/uploads/creator/1/sales.txt', mode='rb') as file:
            response = self.client.post(API_CONTRACTS_URL, {'upload': file})
            self.assertEqual(response.status_code, 302)
            self.assertTrue(Contract.objects.exists())
            contract = Contract.objects.first()
            self.assertEqual(contract.creator, self.user)
            self.assertEqual(contract.status, '1')
            self.assertEqual(contract.upload.name, 'sales.txt')
