from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Contract

from core.utils.data_process import process_file
import os


@receiver(post_save, sender=Contract)
def process_data(sender, instance, **kwargs):
    print("CHAMANDO O SIGNAL PARA INICIAR O PROCESSAMENTO!")
    path = instance.upload.path
    if os.path.isfile(path):
        process_file(path)
