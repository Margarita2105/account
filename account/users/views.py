from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from users.serializers import UserSerializer, UserSignInSerializer
from users.models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['username']
    ordering = ['id']
    lookup_field = 'username'


class GetToken(APIView):

    serializer_class = UserSignInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'token': serializer.get_token()})
