from django.core.management.base import BaseCommand
from transactions.models import Contract
from transactions.models import TransactionType, Transaction, Report
from django.db import DatabaseError, transaction as transaction_atomic
import json
from django.core.cache import cache
from .data_validate import (validate_date_format, validate_price,
                            validate_product, validate_seller,
                            validate_type_id)


class Command(BaseCommand):
    help = 'Call the process data function to extract data from txt and save on DB'

    """
        Django management command to extract data from the txt file,
        treat and send it to the bank, as well as generate a
        small report from the extracted data


        Methods:
        `get_cached_type(self, extracted_id):`
            Checks if the requested type is already cached. If not, it
            retrieves the TransactionType object from the database and
            stores it in the cached_types dictionary, to prevent the
            database from being requested several times during data extraction.

        `add_arguments(self, parser):`
            This method is responsible for defining the arguments that the
            command will accept.
            
            It starts extracting and validating the data, then starts assembling
            the report in json to store the report data, and thus prevent several
            queries with a large number of joins, aggregations and calculations
            from being made in the database to display this data.

            The report is a mirror of the data at the time of processing the file,
            as well as the transactions at the time it will not be possible to change
            without a new upload.

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

    def get_cached_type(self, extracted_id):
        """
            `Method to cache the instance of TransactionType`,
            reducing the number of queries performed in the database.
            Without the cache the number of queries will be the number of lines of the
            file, while with the cached query it will only be 4, which are
            the existing types in the bank currently.
        """

        cached_types = cache.get('transaction_types')
        if cached_types is None:
            cached_types = {}

        if extracted_id not in cached_types:
            transaction_type = TransactionType.objects.get(type=extracted_id)
            cached_types[extracted_id] = transaction_type
            cache.set('transaction_types', cached_types)

        return cached_types[extracted_id]

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='File path')
        parser.add_argument('id', type=int, help='Contract ID')

    @transaction_atomic.atomic
    def handle(self, *args, **kwargs):
        file = kwargs['file']
        contract_id = kwargs['id']

        transactions = []
        sales = {}
        affiliate = {}
        affiliate_final_balance = {}

        with open(file, 'r') as file:
            self.stdout.write(self.style.WARNING(
                "Processing Started..."))

            for line in file:
                type_id = validate_type_id(line[0])
                type = self.get_cached_type(type_id)
                date = validate_date_format(line[1:26])
                product = validate_product(line[26:56])
                price = validate_price(line[56:66])
                seller = validate_seller(line[66:86])

                person = seller.replace(" ", "_")
                product_key = product.replace(" ", "_").replace("-", "_")

                if person not in sales:
                    sales[person] = {}

                if product_key not in affiliate:
                    affiliate[product_key] = {
                        'affiliate': person, 'received': 0, 'sell': 0}

                if type_id == 1:
                    if product_key not in sales[person]:
                        sales[person][product_key] = {
                            'person': person, 'price': 0}

                    sales[person][product_key]['price'] += price

                elif type_id == 2:
                    if product_key in affiliate:
                        affiliate[product_key]['sell'] += price

                elif type_id == 4:
                    affiliate[product_key]['received'] += price

                    if product_key not in affiliate_final_balance:
                        affiliate_final_balance[product_key] = {}

                    if person not in affiliate_final_balance[product_key]:
                        affiliate_final_balance[product_key][person] = 0

                    affiliate_final_balance[product_key][person] += price

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

            for person, product_key in sales.items():
                for product_name, struct in product_key.items():
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
                        'affiliates': affiliate_final_balance[product_name] if product_name in affiliate_final_balance else {}
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

            self.stdout.write(self.style.SUCCESS("Finished processing"))
        except DatabaseError:
            self.stdout.write(self.style.ERROR("Processing error"))
