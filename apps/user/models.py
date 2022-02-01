from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class UserModel(AbstractUser):
    username = None
    user_permissions = None
    first_name = None
    last_name = None
    groups = None
    is_superuser = None
    is_staff = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    user_type = models.CharField(
        max_length=255,
        choices=(
            ("Interno MaisTODOS", "Interno MaisTODOS"),
            ("Empresa X", "Empresa X"),
            ("Empresa Y", "Empresa Y"),
            ("Empresa Z", "Empresa Z"),
        )
    )
    email = models.EmailField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    document = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex="^.{11}$", message="Length must to be 11", code="nomatch"
            )
        ],
        unique=True
    )

    objects = UserManager()

    class Meta:
        managed = True


class CustomerModel(models.Model):
    name = models.CharField(max_length=100)
    document = models.CharField(
        max_length=11,
        validators=[
            RegexValidator(
                regex="^.{11}$", message="Length must to be 11", code="nomatch"
            )
        ]
    )
