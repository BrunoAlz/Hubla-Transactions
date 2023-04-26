from django.db import models
from core.models import User
from django.urls import reverse
from core.utils.file_path import upload_documentos
from core.utils.balance_formater import balance_formater


class Contract(models.Model):

    STATUS = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
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
        upload_to=upload_documentos
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default=""
    )

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return self.creator.first_name


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

    def get_absolute_url(self):
        return reverse("TransactionType_detail", kwargs={"pk": self.pk})


class Seller(models.Model):

    name = models.CharField(
        'Seller name',
        max_length=20
    )

    balance = models.PositiveIntegerField(
        null=True, blank=True
    )

    def __str__(self):
        return f'{self.name}'

    @property
    def formated_balance(self):
        return balance_formater(self.balance)


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

    def __str__(self):
        return f'{self.type} - {self.date} - {self.product} - {self.price} - {self.seller}'

    def get_absolute_url(self):
        return reverse("Transaction_detail", kwargs={"pk": self.pk})
