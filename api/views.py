from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from posts.models import Post
from .serializers import PostSerializer


class ListCreatePostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        posts_serialized = PostSerializer(posts, many=True)
        return Response(posts_serialized.data)

    def post(self, request):
        post = PostSerializer(data=request.data)
        if post.is_valid():
            post.save()
            return Response(post.data)
        return Response('Something went wrong', status=status.HTTP_500_INTERNAL_SERVER_ERROR)