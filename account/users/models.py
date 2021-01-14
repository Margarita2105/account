from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.core import validators


class User(AbstractUser):
    class UserStatus:
        EXECUTOR = 'executor'
        CUSTOMER = 'customer'

        choices = [
            (EXECUTOR, EXECUTOR),
            (CUSTOMER, CUSTOMER),
        ]

    role = models.CharField(max_length=9, choices=UserStatus.choices, default=UserStatus.EXECUTOR)
    bio = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
        )
    balance = models.IntegerField(blank=True, null=True)
    freeze_balance = models.IntegerField(blank=True, null=True)
    confirmation_code = models.CharField(max_length=9)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_token(self):
        refresh = RefreshToken.for_user(self)
        token = str(refresh.access_token)
        return token
