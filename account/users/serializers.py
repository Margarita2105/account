from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'role', 'balance', 'freeze_balance', 'password',)
        model = User

class UserSignInSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=50)
    email = models.EmailField(unique=True)

    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
