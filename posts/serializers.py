from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "author",
            "is_blocked",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("author", "is_blocked")


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "author",
            "is_blocked",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True, source="author.username")

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "content",
            "author",
            "is_blocked",
            "created_at",
            "updated_at"
        )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "content",
            "author",
            "is_blocked",
            "parent_comment",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("author", "is_blocked", "parent_comment")
