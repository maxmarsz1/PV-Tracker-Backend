from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from django.utils.timezone import now

from posts.models import Post
from .serializers import PostSerializer, UserSerializer


def sort_posts(posts):
    months = posts.dates('date', 'month')
    sorted_posts = {}
    for month in months:
        if sorted_posts.get(month.year) is None:
            sorted_posts[month.year] = []
        sorted_posts[month.year].append({month.month: [PostSerializer(post).data for post in posts if post.date.year == month.year and post.date.month == month.month]})
    return sorted_posts


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


class ListCreatePostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        
        # for key, value in sorted_posts.items():
        #     print(key, value)
        
        # posts_serialized = PostSerializer(posts, many=True)
        return Response(sort_posts(posts))

    def post(self, request):
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post.save()
            posts = Post.objects.all()
            return Response(sort_posts(posts))
        return Response('Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateDestroyPostView(APIView):
    def patch(self, request, pk):
        post = Post.objects.get(id=pk)
        serialized = PostSerializer(post, data=request.data, partial=True)
        if serialized.is_valid():
            serialized.save()
            posts = Post.objects.all()
            return Response(sort_posts(posts), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()
        posts = Post.objects.all()
        if post.id is None:
            return Response(sort_posts(posts), status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
