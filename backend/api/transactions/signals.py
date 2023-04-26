from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contract
from django.core.management import call_command
import os


@receiver(post_save, sender=Contract)
def process_data(sender, instance, **kwargs):
    path = instance.upload.path
    contract_id = instance.id
    if os.path.isfile(path):
        print("CHAMANDO O COMMAND PARA INICIAR O PROCESSAMENTO!")
        call_command('call_data_processor', path,
                     int(contract_id), force_color=False)
