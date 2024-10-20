from rest_framework import serializers
from .models import Post, Comment
from .validators import validate_profanity


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    content = serializers.CharField()

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

    def validate(self, data):
        if validate_profanity(data.get('title', '')) or validate_profanity(data.get('content', '')):
            data['is_blocked'] = True
        else:
            data['is_blocked'] = False
        return data


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
    content = serializers.CharField()

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

    def validate(self, data):
        if validate_profanity(data.get('content', '')):
            data['is_blocked'] = True
        else:
            data['is_blocked'] = False
        return data
