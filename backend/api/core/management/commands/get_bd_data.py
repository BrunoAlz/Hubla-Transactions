from django.core.management.base import BaseCommand
from transactions.models import Contract
from django.core.management import call_command

# REFERÊNCIA
# https://simpleisbetterthancomplex.com/tutorial/2018/08/27/how-to-create-custom-django-management-commands.html
# https://docs.djangoproject.com/id/4.0/_modules/django/core/management/base/

# TODO, VOLTAR E VER SE DA PARA MELHORA MAIS, COMENTAR EM INGLÊS nA REVISÃO


class Command(BaseCommand):

    """
        Esta função é um command do proprio django, que pode ser chamado no
        terminal com o comando `python manage.py XXXXXXXX.py` ele execulta
        o arquivo chamado via terminal, e `Execulta o que está na handle`

        TODO, 1 - Comentar tudo o que está acontecendo. 2 - após ter algo no front
        voltar aqui para melhorar a estrutura.
    """
    help = 'Call the process data function to extract data from txt and save on DB'
    # Metadata about this command.

    def handle(self, *args, **kwargs):
        # Verifica com o exists por que é mais rápido pegar só 1 para testar
        check_pending = Contract.objects.filter(status=1).exists()
        if check_pending:
            # Se encontrar um, pega todos e Processa.
            pending = Contract.objects.filter(status=1)
            for data in pending:
                # Impre no terminal a Mensagem de Processamento
                self.stdout.write(self.style.WARNING(
                    f"Processando os Contrato: {data.id}"))

                call_command('call_data_processor', data.upload.path,
                             int(data.id), force_color=False)
                # Quando iniciar o Processamento, atualiza status para 2
                pending.update(status=2)
                # Retorna a Mensagem de sucesso no console.
                self.stdout.write(self.style.SUCCESS(
                    f"O Contrato: {data.id} foi Processado!"))

        else:
            # Caso a verificação falhe, imprime a mensagem.
            self.stdout.write(self.style.WARNING(
                f"Não há transações para serem processadas"))
