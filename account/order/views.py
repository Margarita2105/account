from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, get_object_or_404

from order.models import Post, Respond
from setting.permission import IsOwnerOrReadOnly
from order.serializers import PostSerializer, Responderializer
from users.models import User


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        

class RespondList(ListCreateAPIView):
    queryset = Respond.objects.all()
    serializer_class = RespondSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=executor__username', '=post__name']
