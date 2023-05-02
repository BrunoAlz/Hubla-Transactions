from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db import models


class User(AbstractUser):

    """
        Creates the user model, which will be the table in the database
        responsible for storing the data of users
    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.id
