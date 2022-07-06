from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_superuser(self, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(password, **other_fields)

    def create_user(self, password, **other_fields):

        other_fields.setdefault("is_staff", False)
        other_fields.setdefault("is_superuser", False)
        other_fields.setdefault("is_active", True)

        user = self.model(**other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("email address", unique=True)
    username = models.CharField(max_length=40, unique=True)
    name = models.CharField("first name", max_length=50)
    mobile = models.BigIntegerField()

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "mobile"]

    def __str__(self):
        return self.username


