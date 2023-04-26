import django
from core.management.commands.call_data_processor import Command
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configurations.settings")
django.setup()

comando = Command()
comando.handle(
    {"file": "/sales.txt", "id": "1"})
