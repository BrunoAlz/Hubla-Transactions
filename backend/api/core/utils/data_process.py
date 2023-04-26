from transactions.models import Transaction, TransactionType
from datetime import datetime


def date_formarter(data):
    data_iso = datetime.fromisoformat(data)
    data_formatada = data_iso.strftime("%Y-%m-%dT%H:%M:%SGMT%z")

    return str(data_formatada)


def process_file(file, id):

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
