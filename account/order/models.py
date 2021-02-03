from django.contrib.auth import get_user_model
from django.db import models

from users.models import User


def user_directory_path(instance, filename):
    return 'author_{0}/{1}'.format(instance.author.id, filename)

       
class Post(models.Model):
    class PostStatus:
        ACTIVE = 'active'
        UNAVAILABLE = 'unavailable'
        NEW = 'new'
        DELETE = 'delete'
        MADE = 'made'

        choices = [
            (ACTIVE, ACTIVE),
            (UNAVAILABLE, UNAVAILABLE),
            (NEW, NEW),
            (DELETE, DELETE),
            (MADE, MADE),
        ]

    name = models.CharField(max_length=200)
    text = models.TextField()
    files = models.FileField(upload_to=user_directory_path)
    price = models.PositiveIntegerField(blank=True, null=True)
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    update_date = models.DateTimeField("Дата обновления", auto_now=True)
    expiration_date = models.DateTimeField("Крайний срок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer")
    status = models.CharField(max_length=15, choices=PostStatus.choices, default=PostStatus.NEW)
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="executor", default=None)

    def __str__(self):
        return self.name


class Respond(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="executor")

    class Meta:
        unique_together = "post", "executor"
        
    def __str__(self):
        return self.executor
