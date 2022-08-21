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


class UpdateDestroyPostView(APIView):
    def put(self, request, pk):
        post = Post.objects.get(id=pk)
        serialized = PostSerializer(data=request.data, instance=post)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = Post.objects.get(id=pk)
        post.delete()
        if post.id is None:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
