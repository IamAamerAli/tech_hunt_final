from django.contrib.auth.models import User
from numpy.core.defchararray import rstrip
from rest_framework import serializers

from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='author.username', read_only=True)
    user_id = serializers.CharField(source='author.id', read_only=True)
    image = serializers.CharField(source='author.profile.image', read_only=True)

    class Meta:
        model = Post
        fields = ['user_id', 'user', 'image', 'title', 'content', 'date_posted', 'author']
