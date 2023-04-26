from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Contract(models.Model):

    creator = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    upload = models.FileField(
        'Document'
    )

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    def __str__(self):
        return self.creator

    def get_absolute_url(self):
        return reverse("Contract_detail", kwargs={"pk": self.pk})
