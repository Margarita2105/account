import secrets

from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import UserSerializer

from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    ordering = ['id']
    lookup_field = 'username'


class MyProfile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class GetToken(APIView):

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email, password=password)
            user.is_active = True
            user.save()
            return Response({'token': user.get_token()})

        except User.DoesNotExist:
            return Response(
                data={'detail': 'Пользователя с такими данными не существует'},
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get('email')
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            User.objects.update_or_create(
                defaults={'password': password},
                email=email, username=username
            )

            send_mail(
                'Registration',
                'Your confirmation code is ' + str(confirmation_code),
                'from@gmail.com',
                [str(email)],
                fail_silently=False,
            )
            return Response({'details': 'Код подтверждения выслан вам на почту'},
                status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
