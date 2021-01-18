from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from rest_framework.authtoken.models import Token


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    class UserStatus:
        EXECUTOR = 'executor'
        CUSTOMER = 'customer'

        choices = [
            (EXECUTOR, EXECUTOR),
            (CUSTOMER, CUSTOMER),
        ]

    role = models.CharField(max_length=9, choices=UserStatus.choices, default=UserStatus.EXECUTOR)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    balance = models.PositiveIntegerField(blank=True, null=True)
    freeze_balance = models.PositiveIntegerField(blank=True, null=True)
    password = models.CharField(max_length=50)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_token(self):
        token, created = Token.objects.get_or_create(user=user)
        return token.key
