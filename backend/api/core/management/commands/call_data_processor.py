from django.core.management.base import BaseCommand
from transactions.models import Contract
from transactions.models import TransactionType, Transaction, Report
from django.db import DatabaseError, transaction as transaction_atomic
import json


class Command(BaseCommand):
    help = 'Call the process data function to extract data from txt and save on DB'

    """
        Django management command to extract data from the txt file,
        treat and send it to the bank, as well as generate a
        small report from the extracted data


        Methods:
        `add_arguments(self, parser):`
            This method is responsible for defining the arguments that the
            command will accept.
            
            It receives a parser object as a parameter,
            which must be used to add arguments using the add_argument method.
            In this case, the command takes two mandatory arguments: file and id.
            What are the data generated after uploading a file.

        `def handle(self, *args, **kwargs):`
            This method is responsible for executing the main `logic of the
            command`.
            
            It is called when the command is executed and receives
            the arguments defined in the add_arguments method as a kwargs dictionary.
            The main logic of the command is to process a text file and save
            the extracted data in the database.

            The method uses the `transaction_atomic.atomic decorator` to ensure
            that all database operations are performed within a single atomic
            transaction, i.e. if an error occurs in any of the database operations,
            all operations are rolled back.
    """

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Caminho do Arquivo')
        parser.add_argument('id', type=int, help='Id do Contrato')

    @transaction_atomic.atomic
    def handle(self, *args, **kwargs):
        file = kwargs['file']
        contract_id = kwargs['id']

        transactions = []
        sales = {}
        affiliate = {}

        """
            TXT data extraction
        """
        with open(file, 'r') as file:
            self.stdout.write(self.style.WARNING(
                "Processamento Iniciado..."))

            for line in file:
                type_id = int(line[0])
                type = TransactionType.objects.get(type=type_id)
                date = line[1:26].replace(" ", "")
                product = line[26:56].strip()
                price = int(line[56:66])
                seller = line[66:86].strip()
                person = seller.replace(" ", "_")

                if person not in sales:
                    sales[person] = {}

                if product not in affiliate:
                    affiliate[product] = {
                        'affiliate': person, 'received': 0, 'sell': 0}

                if type_id == 1:
                    if product not in sales[person]:
                        sales[person][product] = {
                            'person': person, 'price': 0}

                    sales[person][product]['price'] += price

                elif type_id == 2:
                    if product in affiliate:
                        affiliate[product]['sell'] += price

                elif type_id == 4:
                    affiliate[product]['received'] += price

                transaction = Transaction(
                    type=type,
                    date=date,
                    product=product,
                    price=price,
                    seller=seller,
                    contract_id=contract_id
                )
                transactions.append(transaction)

            report_total = []

            for person, product in sales.items():
                for product_name, struct in product.items():
                    sold_by_affiliate = 0
                    total_commission_paid = 0
                    if product_name in affiliate:
                        sold_by_affiliate = affiliate[product_name]['sell']
                        total_commission_paid = affiliate[product_name]['received']

                    gross_total = struct['price'] + sold_by_affiliate
                    result = {
                        'person': person,
                        'product': product_name,
                        'total_sold_by_producer': struct['price'],
                        'total_sold_by_affiliate': sold_by_affiliate,
                        'total_commission_paid': total_commission_paid,
                        'gross_total': gross_total,
                        'liquid': gross_total - total_commission_paid,

                    }
                    report_total.append(result)
            data_json = json.dumps(report_total)

        try:
            Report.objects.update_or_create(
                contract_id=contract_id,
                report_data=data_json
            )

            Transaction.objects.bulk_create(transactions)

            Contract.objects.filter(id=contract_id).update(
                status=3)

            self.stdout.write(self.style.SUCCESS("Processamento Finalizado!"))
        except DatabaseError:
            self.stdout.write(self.style.ERROR("Erro no processamento"))
