from rest_framework import serializers

from .models import Post, Respond


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = '__all__'
        model = Post


class RespondSerializer(serializers.ModelSerializer):
    post = serializers.ReadOnlyField(source='post.name')
    executor = serializers.ReadOnlyField(source='executor.username')
    
    class Meta:
        fields = ('post', 'executor')
        model = Respond
        