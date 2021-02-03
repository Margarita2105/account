from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.response import Response

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

    def perform_update(self, serializer):
        executor = get_object_or_404(Respond, pk=self.kwargs.get('respondlist_id'))
        serializer.save(author=self.request.user, executor=executor)

class RespondList(ListCreateAPIView):
    queryset = Respond.objects.all()
    serializer_class = RespondSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=executor__username', '=post__name']

class RespondListView(viewsets.ViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def list(self, request):
        executors = Respond.objects.filter(post.author=self.request.user).values_list("executor_id", flat=True)
        queryset = User.objects.filter(id__in=executors).all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        executor = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(executor)
        return Response(serializer.data)
