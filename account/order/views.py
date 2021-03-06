from django.db import transaction
from django.db.models import F
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

    @action(methods=['POST'], detail=True, permission_classes=[IsOwnerOrReadOnly,])
    def approve(self, request, pk, executor_pk, *args, **kwargs):
        data = {
            'executor_pk': request.data.get('executor_pk'),
            'post_pk': pk,
        }
        serializer = Serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @classmethod
    def transactionfunc(cls, post_pk):
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=post_pk)
            try:
                post.author.freeze_balance = post.price
                post.author.balance = F('balance') - post.price
                post.author.save()
                status = 'success'
            except:
                status = 'Failed'
            tr = cls(
                author=post.author.email,
                price=post.price,
                status=status,
            )
        return tr

    @classmethod
    def payfunc(cls, post_pk):
        with transaction.atomic():
            post = Post.objects.select_for_update().get(pk=post_pk)
            try:
                post.author.freeze_balance = F('freeze_balance') - post.price
                post.author.save()

                post.executor.balance = F('balance') + post.price
                post.executor.save()

                status = 'success'
            except:
                status = 'Failed'
            tr = cls(
                author=post.author.email,
                executor=post.executor.email
                price=post.price,
                status=status,
                type='pay',
            )
        return tr

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
