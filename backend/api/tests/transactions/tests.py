from rest_framework.test import APIClient, APITestCase
from user.models import User
from transactions.models import Contract
from user.authentication import JWTAuthentucation
from tests.constants import (TEST_EMAIL, TEST_PASSW, API_CONTRACTS_URL)


class ContractCreateViewTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        user = self.user = User.objects.create_user(
            email=TEST_EMAIL, password=TEST_PASSW)
        self.token = JWTAuthentucation.generate_jwt(user.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('TESTANDO CONTRACT CREATION VIEW\n')
        f.close()
        f = open(path, 'rb')
        return {'upload': f}

    def test_create_contract_successful(self):
        upload = self._create_test_file('sales.txt')
        response = self.client.post(
            API_CONTRACTS_URL, upload, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Contract.objects.exists())
        contract = Contract.objects.first()
        self.assertEqual(contract.creator, self.user)
        self.assertEqual(contract.status, '1')
        self.assertEqual(contract.upload.name,
                         'api/uploads/creator/1/sales.txt')
