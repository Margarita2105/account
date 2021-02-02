from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order.views import PostViewSet, RespondList


router = DefaultRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<posts_id>\d+)/respondlist', RespondListView, basename='respondlist')

urlpatterns = [
    path('respond/', RespondList.as_view()),
    path('', include(router.urls)),
]
