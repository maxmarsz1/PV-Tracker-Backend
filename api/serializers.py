from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User

from posts.models import Post
from user_settings.models import UserConfig


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class UserConfigSerializer(ModelSerializer):
    class Meta:
        model = UserConfig
        fields = '__all__'



class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']