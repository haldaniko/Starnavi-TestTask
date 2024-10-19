from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from profanity_check import predict


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_profanity(content):
        return predict([content])[0] == 1

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        content = data.get('content', '')
        title = data.get('title', '')

        has_profanity = self.check_profanity(content) or self.check_profanity(title)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save(author=request.user)

        if has_profanity:
            instance.is_blocked = True
            instance.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()

        content = data.get('content', '')
        title = data.get('title', '')

        has_profanity = self.check_profanity(content) or self.check_profanity(title)

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if has_profanity:
            instance.is_blocked = True
            instance.save()

        return Response(serializer.data)


class PostViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(BaseViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer