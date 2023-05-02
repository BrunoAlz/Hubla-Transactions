from django.db import models
from user.models import User
from core.utils.file_path import upload_documentos
from django.core.validators import FileExtensionValidator
from datetime import datetime


class Contract(models.Model):

    STATUS = (
        ("1", "Pendente"),
        ("2", "Processando"),
        ("3", "Processado"),
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    upload = models.FileField(
        'Document',
        upload_to=upload_documentos,
        validators=[FileExtensionValidator(allowed_extensions=["txt"])]
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default="1"
    )

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return f"{self.creator.first_name} {self.creator.last_name}"

    @property
    def get_creator_full_name(self):
        full_name = f"{self.creator.first_name} {self.creator.last_name}"
        return full_name


class TransactionType(models.Model):

    NATURE = (
        ("Entrada", "Entrada"),
        ("Saida", "Saída"),
    )

    SIGNAL = (
        ("+", "+"),
        ("-", "-"),
    )

    type = models.SmallIntegerField(
    )

    description = models.CharField(
        'Description',
        max_length=20
    )

    nature = models.CharField(
        max_length=20,
        choices=NATURE,
        default="Entrada"
    )

    signal = models.CharField(
        max_length=1,
        choices=SIGNAL,
        default=" "
    )

    class Meta:
        verbose_name = ("TransactionType")
        verbose_name_plural = ("TransactionTypes")

    def __str__(self):
        return f'{self.type} - {self.description} - {self.nature} - {self.signal}'


class Seller(models.Model):

    name = models.CharField(
        'Seller name',
        max_length=20
    )

    role = models.CharField(
        'Seller role',
        max_length=20
    )

    def __str__(self):
        return f'{self.name}'


class Transaction(models.Model):

    type = models.ForeignKey(
        TransactionType,
        on_delete=models.DO_NOTHING,
        related_name='transaction_type'
    )

    contract = models.ForeignKey(
        Contract,
        on_delete=models.DO_NOTHING,
        related_name='transactio_contract'
    )

    date = models.DateTimeField(
        'date',
    )

    product = models.CharField(
        'product',
        max_length=30,
    )

    price = models.PositiveIntegerField(
        null=True, blank=True
    )

    seller = models.CharField(
        'seller',
        max_length=20,
        null=True, blank=True
    )

    class Meta:
        verbose_name = ("Transaction")
        verbose_name_plural = ("Transactions")
        ordering = ['type']

    def __str__(self):
        return f'{self.type} - {self.date} - {self.product} - {self.price} - {self.seller}'

    def date_formarter(self):
        data_iso = datetime.fromisoformat(self.date)
        data_formatada = data_iso.strftime("%Y-%m-%dT%H:%M:%SGMT%z")
        return data_formatada


class Report(models.Model):

    contract = models.ForeignKey(
        Contract,
        on_delete=models.DO_NOTHING,
        related_name='report'
    )

    report_data = models.JSONField(
        'report data'
    )

    class Meta:
        verbose_name = ("report")
        verbose_name_plural = ("reports")
