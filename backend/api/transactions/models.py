from django.db import models
from core.models import User
from django.urls import reverse
from core.utils.file_path import upload_documentos


class Contract(models.Model):

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

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return self.creator

    def get_absolute_url(self):
        return reverse("Contract_detail", kwargs={"pk": self.pk})
