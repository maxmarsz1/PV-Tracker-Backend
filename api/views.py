from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.timezone import now

from posts.models import Post
from user_settings.models import UserConfig
from .serializers import PostSerializer, UserSerializer, UserConfigSerializer
from .utils import prepare_posts



class UserRegisterView(APIView):
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(username=username).first(): return Response('Nazwa użytkownika zajęta', status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).first(): return Response('Adres email zajęty', status=status.HTTP_400_BAD_REQUEST)
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return Response(status=status.HTTP_201_CREATED)


class UserConfigView(APIView):
    def get(self, request, pk):
        # Secure this when user auth will be included
        # config = UserConfig.objects.get(user=request.user)
        config = UserConfig.objects.get(user__id=pk)
        serialized = UserConfigSerializer(config)
        return Response(serialized.data)

    def patch(self, request, pk):
        # Secure this when user auth will be included
        # config = UserConfig.objects.get(user=request.user)
        config = UserConfig.objects.get(user__id=pk)
        serialized = UserConfigSerializer(config, request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data)
        print(serialized.errors)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreatePostView(APIView):
    def post(self, request):
        post = PostSerializer(data=request.data, partial=True)
        if post.is_valid():
            post = post.save()
            posts = Post.objects.filter(date__year=post.date.year)
            return Response(prepare_posts(posts))
        print(post.errors)
        return Response('Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def patch(self, request):
        print(Post.objects.filter(user__id=1).order_by('date'))
        last_post = Post.objects.filter(user__id=1).order_by('date').first()
        last_post.save(recalculate=True)
        posts = Post.objects.filter(date__year=request.data['year'])
        return Response(prepare_posts(posts))


class ListUpdateDestroyPostView(APIView):
    def get(self, request, pk):
        posts = Post.objects.filter(date__year=pk)
        return Response({'posts': prepare_posts(posts)})


    def patch(self, request, pk):
        post = Post.objects.get(id=pk)
        post_serialized = PostSerializer(post, data=request.data, partial=True)
        if post_serialized.is_valid():
            post_serialized.save()
            posts = Post.objects.filter(date__year=post.date.year)
            return Response(prepare_posts(posts))
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()
        if post.id is None:
            return Response()
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
