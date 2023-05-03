from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class UserManager(BaseUserManager):
    """
    `UserManager` is a class that extends `BaseUserManager`, a Django class that
     defines the default model manager for the User model. The purpose of
     UserManager is to provide custom methods to create users.
    """

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(("You must provide a valid email address"))

    def create_user(
        self, email, password, **extra_fields
    ):
        if not email:
            raise ValueError(("Users must submit a email"))

        if not password:
            raise ValueError(("Users must submit a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(
                ("Base User Account: An email address is required"))

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):

    """
        Creates the user model, which will be the table in the database
        responsible for storing the data of users
    """

    first_name = models.CharField(
        max_length=255)

    last_name = models.CharField(
        max_length=255)

    email = models.CharField(
        max_length=255,
        unique=True,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )

    password = models.CharField(
        max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.id
