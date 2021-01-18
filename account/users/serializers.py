from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'balance', 'freeze_balance', 'password',)
        model = User