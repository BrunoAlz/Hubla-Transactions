from django.core.management.base import BaseCommand
from transactions.models import TransactionType, Transaction


# REFERÊNCIA
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
# https://docs.djangoproject.com/id/4.0/_modules/django/core/management/base/

class Command(BaseCommand):
    help = 'Call the process data function to extract data from txt and save on DB'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Caminho do Arquivo')
        parser.add_argument('id', type=int, help='Id do Contrato')

    def handle(self, *args, **kwargs):
        file = kwargs['file']
        id = kwargs['id']

        transactions = []

        with open(file, 'r') as file:
            print("Processamento Iniciado .. .. ..")

            for line in file:
                type_id = int(line[0])
                type = TransactionType.objects.get(type=type_id)
                date = line[1:26].replace(" ", "")
                product = line[26:56].strip()
                price = int(line[56:66])
                seller = line[66:86].strip()

                transaction = Transaction(
                    type=type,
                    date=date,
                    product=product,
                    price=price,
                    seller=seller,
                    contract_id=id
                )
                transactions.append(transaction)

        Transaction.objects.bulk_create(transactions)
        print("Processamento Finalizado")
