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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "content",
            "author",
            "is_blocked",
            "created_at",
            "updated_at"
        )
        read_only_fields = ("author", "is_blocked",)
