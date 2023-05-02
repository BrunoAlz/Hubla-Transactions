from django.core.management.base import BaseCommand
from transactions.models import Contract
from django.core.management import call_command


class Command(BaseCommand):
    """
        Django management command that verify pending contract.

        `handle` checks the database for contracts
         pending, if it exists, search for contracts and send them to the
         function of processing.
    """

    def handle(self, *args, **kwargs):
        check_pending = Contract.objects.filter(status=1).exists()
        if check_pending:
            pending = Contract.objects.filter(status=1)
            for data in pending:
                self.stdout.write(self.style.WARNING(
                    f"Processing the Contract: {data.id}"))

                call_command('call_data_processor', data.upload.path,
                             int(data.id), force_color=False)

                self.stdout.write(self.style.SUCCESS(
                    f"The Contract: {data.id} has been Processed!"))

        else:

            self.stdout.write(self.style.WARNING(
                "There are no transactions to be processed"))
