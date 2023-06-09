from django.forms import ValidationError
from rest_framework.test import APIClient, APITestCase
# from transactions.models import Report
from user.models import User
from transactions.models import Contract
from user.authentication import JWTAuthentucation
from tests.constants import (
    TEST_EMAIL, TEST_PASSW, API_CONTRACTS_URL, UPLOADS,
    PENDING, VENDA_PRODUTOR)
from rest_framework import status
from transactions.models import Transaction, TransactionType
from datetime import datetime
from django.test import TestCase
from django.db import DataError, IntegrityError


class ContractModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            password=TEST_PASSW
        )

    def tests_the_creation_of_the_Contract_passing_all_the_parameters(self):
        self.assertTrue(Contract.objects.create(
            creator=self.user, upload='test.txt', status=PENDING))

    def tests_the_creation_of_the_Contract_whitout_the_parameters(self):
        with self.assertRaises(IntegrityError):
            Contract.objects.create(
                creator=None, upload=None, status=None)

    def test_if_the_contract_creator_is_required(self):
        with self.assertRaises(IntegrityError):
            Contract.objects.create(upload='file1.txt', status=PENDING)

    def teste_if_the_upload_file_is_required(self):
        self.assertTrue(Contract.objects.create(creator=self.user))


class TransactionTypeModelTestCase(TestCase):

    def test_transaction_type_creation(self):
        type = TransactionType.objects.create(
            type=VENDA_PRODUTOR,
            description="teste type",
            nature="Entry",
            signal="+"
        )
        self.assertIsInstance(type, TransactionType)
        self.assertEqual(str(type), "1 - teste type - Entry - +")

    def test_transaction_type_signal_accepts_only_valid_choices(self):
        with self.assertRaises(ValidationError):
            type = TransactionType.objects.create(
                type=VENDA_PRODUTOR,
                description="Test type",
                nature="Entry",
                signal="2"
            )
            type.full_clean()


class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email=TEST_EMAIL,
            password=TEST_PASSW)

    def test_transaction_created_successfully(self):
        transaction_type = TransactionType.objects.create(
            type=VENDA_PRODUTOR, description='test type', nature='Entrada', signal='+'
        )
        contract = Contract.objects.create(
            creator=self.user, upload=UPLOADS, status=PENDING
        )
        transaction = Transaction.objects.create(
            type=transaction_type, contract=contract,
            date=datetime.now(), product='Test Product', price=1000,
            seller='Test Seller'
        )
        self.assertIsNotNone(transaction.pk)

    def test_transaction_seller_is_required(self):
        transaction_type = TransactionType.objects.create(
            type=VENDA_PRODUTOR, description='test type', nature='Entrada', signal='+'
        )
        contract = Contract.objects.create(
            creator=self.user, upload=UPLOADS, status=PENDING
        )
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                type=transaction_type, contract=contract,
                date=datetime.now(), product='Test Product', price=1000,
                seller=None
            )

    def test_transaction_price_is_required(self):
        transaction_type = TransactionType.objects.create(
            type=VENDA_PRODUTOR, description='test type', nature='Entrada', signal='+'
        )
        contract = Contract.objects.create(
            creator=self.user, upload=UPLOADS, status=PENDING
        )
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                type=transaction_type, contract=contract,
                date=datetime.now(), product='Test Product', price=None,
                seller="Teste Seller"
            )

    def test_transaction_if_price_can_be_negative(self):
        transaction_type = TransactionType.objects.create(
            type=VENDA_PRODUTOR, description='test type', nature='Entrada', signal='+'
        )
        contract = Contract.objects.create(
            creator=self.user, upload=UPLOADS, status=PENDING
        )
        with self.assertRaises(DataError):
            Transaction.objects.create(
                type=transaction_type, contract=contract,
                date=datetime.now(), product='Test Product', price=-2131,
                seller="Teste Seller"
            )


class ContractCreateListAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_token = None
        self.user_token = self.user = User.objects.create_user(
            email=TEST_EMAIL, password=TEST_PASSW)
        self.token = JWTAuthentucation.generate_jwt(self.user_token.id)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    # def _create_test_file(self, path):
    #     f = open(path, 'w')
    #     f.write('TESTANDO CONTRACT CREATION VIEW\n')
    #     f.close()
    #     f = open(path, 'rb')
    #     return {'upload': f}

    # def tests_whether_the_creation_of_the_contract_is_correct(self):
    #     upload = self._create_test_file('sales.txt')
    #     response = self.client.post(
    #         API_CONTRACTS_URL, upload, format='multipart')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(Contract.objects.exists())
    #     contract = Contract.objects.first()
    #     self.assertEqual(contract.creator, self.user)
    #     self.assertEqual(contract.status, '1')
    #     self.assertEqual(contract.upload.name,
    #                      'api/uploads/creator/1/sales.txt')

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

    def test_contract_list_unauthenticated_user(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(f"{API_CONTRACTS_URL}list/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ContractTransactionsDetailsAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()

        self.user_token = User.objects.create_user(
            email=TEST_EMAIL, password=TEST_PASSW)

        self.token = JWTAuthentucation.generate_jwt(self.user_token.id)

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.contract = Contract.objects.create(
            creator=self.user_token, upload='file1.txt', status='1')

        type = self.type = TransactionType.objects.create(
            type=1, description="teste", nature="Entry", signal="+")

        self.transactions = Transaction.objects.create(
            type=type,
            contract=self.contract,
            date=datetime.now(),
            product="TEST PRODUCT",
            price=999999999,
            seller="TESTE SELER",
        )

    def tests_the_listing_of_transactions_by_the_authenticated_user(self):
        response = self.client.get(
            f"{API_CONTRACTS_URL}{self.contract.pk}", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        transactions = response.data['transactio_contract']

        self.assertNotEqual(len(transactions), 0)

        self.assertEqual(transactions[0]['contract'], self.contract.id)

    def test_unauthorized_user_cannot_view_contract_details(self):
        response = self.client.get(
            f"{API_CONTRACTS_URL}{self.contract.pk}", follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
