from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from profanity_check import predict


class BaseViewSet(viewsets.ModelViewSet):
    @staticmethod
    def check_profanity(content):
        if predict([content])[0] == 1:
            return Response(
                {"detail": "Content contains inappropriate language."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def create(self, request, *args, **kwargs):
        content = request.data.get('content', '')
        title = request.data.get('title', '')
        response = self.check_profanity(content) or self.check_profanity(title)
        if response:
            return response
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        content = request.data.get('content', '')
        title = request.data.get('title', '')
        response = self.check_profanity(content) or self.check_profanity(title)
        if response:
            return response
        return super().update(request, *args, **kwargs)


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
