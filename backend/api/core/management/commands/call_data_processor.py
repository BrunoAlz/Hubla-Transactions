from django.core.management.base import BaseCommand
from transactions.models import Contract
from transactions.models import TransactionType, Transaction, Seller
from django.db import DatabaseError, transaction as transaction_atomic

# REFERÊNCIA
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
# https://docs.djangoproject.com/id/4.0/_modules/django/core/management/base/


class Command(BaseCommand):
    help = 'Call the process data function to extract data from txt and save on DB'

    def create_producer_and_affiliate(self, id_seller: int, seller_name: str) -> None:
        if id_seller == 1:
            Seller.objects.update_or_create(
                name=seller_name, role="Producer")
        elif id_seller == 2:
            Seller.objects.update_or_create(
                name=seller_name, role="Affiliate")
        else:
            pass

    def add_arguments(self, parser):
        """Recebe os argumentos passados pelo `get_bd_data`
        data.upload.path, int(data.id) """
        parser.add_argument('file', type=str, help='Caminho do Arquivo')
        parser.add_argument('id', type=int, help='Id do Contrato')

    # Chama o Decorador `atomic do django` para que a consulta seja processada
    # De forma atomica, visto que se trada de uma Lista de Transações, que
    # Envolvem dinheiro
    @transaction_atomic.atomic
    def handle(self, *args, **kwargs):
        # Recupera os dados passados pelo get_bd_data
        file = kwargs['file']
        contract_id = kwargs['id']

        # Cria uma lista vasia que ira guardar os objetos Transactions
        transactions = []
        sales = {}
        affiliate = {}

        # Com abre o arquivo utilizando o Context Manager With no modo 'R'EAD
        with open(file, 'r') as file:
            # Mostra no console que o processamento foi iniciado
            self.stdout.write(self.style.WARNING(
                "Processamento Iniciado..."))
            # TODO, fazer validações nesses dados, caso a linha venha quebrada ou algo do tipo
            # continuar o processamento e notificar sobre o problema.
            # Começa a percorrer o arquivo txt.
            for line in file:
                # Extrai o primeiro caracter do arquivo, que é um Inteiro e se refere ao TIPO DE TRANSAÇÃO
                type_id = int(line[0])
                # Busca no banco uma `INSTANCIA DO TransactionType` onde o field "type" = TIPO DE TRANSAÇÃO"
                type = TransactionType.objects.get(type=type_id)
                # TODO, arrumar a data com o GMT
                # Extrai a data removendo os espaços em branco que ela possui
                date = line[1:26].replace(" ", "")
                # Extrai o nome do Produto
                product = line[26:56].strip()
                # Extrai o valor do Produto
                price = int(line[56:66])
                # Extrai o Nome do vendedor
                seller = line[66:86].strip()
                person = seller.replace(" ", "_")

                self.create_producer_and_affiliate(type_id, seller)

                if person not in sales:
                    sales[person] = {}

                if product not in affiliate:
                    affiliate[product] = {
                        'affiliate': person, 'recivied': 0, 'sell': 0}

                if type_id == 1:
                    if product not in sales[person]:
                        sales[person][product] = {
                            'person': person, 'price': 0}

                    sales[person][product]['price'] += price

                elif type_id == 2:
                    if product in affiliate:
                        affiliate[product]['sell'] += price

                elif type_id == 4:
                    affiliate[product]['recivied'] += price
                """
                    Após fazer os tratamentos necessários, para cada linha
                    do Txt cria uma instância do Objeto `Transaction` que é 
                    uma Model e armazena da variavel `transaction`
                """
                transaction = Transaction(
                    type=type,  # Talvez mudar o nome das var para "txt_xxxx"
                    date=date,
                    product=product,
                    price=price,
                    seller=seller,
                    contract_id=contract_id
                )
                # Após a criação do Objeto, faz o append na lista de transactions
                transactions.append(transaction)
        # Inicia um bloco Try para tentar fazer o Insert no banco
            report_total = []

            for person, product in sales.items():
                for product_name, struct in product.items():
                    total_sell_affiliate = 0
                    total_comission_payed = 0
                    if product_name in affiliate:
                        total_sell_affiliate = affiliate[product_name]['sell']
                        total_comission_payed = affiliate[product_name]['recivied']

                    total_bruto = struct['price'] + total_sell_affiliate
                    result = {
                        'total_sell_affiliate': total_sell_affiliate,
                        'total_comission_payed': total_comission_payed,
                        'total': total_bruto,
                        'liquido': total_bruto - total_comission_payed,
                        'product': product_name,
                        'total_sell_productor': struct['price'],
                        'peson': person,

                    }
                    report_total.append(result)

        try:
            # O Bulk create irá comitar a transação inteira de uma vez.
            # Escrevendo apenas uma consulta.
            Transaction.objects.bulk_create(transactions)
            # Consulta o Contrato o qual as transações pertencem e
            # Atualiza o seu status para Processado
            # TODO, Mudar o status 3 para uma CONSTANT depois
            Contract.objects.filter(id=contract_id).update(status=3)

            # Impre no terminal a Mensagem de sucesso
            self.stdout.write(self.style.SUCCESS("Processamento Finalizado!"))
        except DatabaseError:
            # Impre no terminal a Mensagem de erro
            self.stdout.write(self.style.ERROR("Erro no processamento"))
