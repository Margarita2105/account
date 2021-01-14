from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework.authtoken.models import Token
from django.core import validators


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_token(self):
        token = Token.objects.create(user=user)
        return token.key
