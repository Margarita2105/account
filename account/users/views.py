from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response

from users.serializers import UserSerializer

from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    ordering = ['id']
    lookup_field = 'username'


class GetToken(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = get_object_or_404(User, email=email, password=password)
            user.is_active = True
            user.save()
            return Response({'token': user.get_token()})

        except User.DoesNotExist:
            return Response(
                data={'detail': 'Пользователя с такими данными не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )
