from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, exceptions

from blog.models import Post


# region PostSerializer
class PostSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source='author.username', read_only=True)
    # user_id = serializers.CharField(source='author.id', read_only=True)
    # image = serializers.CharField(source='author.profile.image', read_only=True)
    # 'user_id', 'user', 'image',
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['title', 'content', 'date_posted', 'author', ]


# endregion

# region UserSerializer
class UserSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'posts', ]


# endregion

# region Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is Inactive"
                    raise exceptions.ValidationError(msg)
            else:
                msg = "Unable to login"
                raise exceptions.ValidationError(msg)
        else:
            msg = "Please Enter Username and Password"
            raise exceptions.ValidationError(msg)
        return data
# endregion
