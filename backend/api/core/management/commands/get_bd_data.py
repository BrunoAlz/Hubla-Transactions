from django.core.management.base import BaseCommand
from transactions.models import Contract
from django.core.management import call_command

# REFERÊNCIA
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
# https://docs.djangoproject.com/id/4.0/_modules/django/core/management/base/


class Command(BaseCommand):
    help = 'Call the process data function to extract data from txt and save on DB'

    # def add_arguments(self, parser):
    #     parser.add_argument('file', type=str, help='Caminho do Arquivo')
    #     parser.add_argument('id', type=int, help='Id do Contrato')

    def handle(self, *args, **kwargs):
        pending = Contract.objects.filter(status=1)
        for data in pending:
            print(
                f"CHAMANDO O COMMAND PARA INICIAR O PROCESSAMENTO! {data.id}")
            call_command('call_data_processor', data.upload.path,
                         int(data.id), force_color=False)
