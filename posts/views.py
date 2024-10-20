from django.db.models import Count, Q
from django.db.models.functions import TruncDate
from django.utils.dateparse import parse_date
from rest_framework import viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer, PostDetailSerializer, PostListSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "list":
            return PostListSerializer
        return PostSerializer


class CommentListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise NotFound('Post not found.')

        return post.comments.all()

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)


class CommentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


@extend_schema(
    operation_id="comments_daily_breakdown",
    summary="Retrieve daily breakdown of comments",
    description=(
            """This API endpoint provides a daily breakdown of comments within a specified date range, including the
            total number of comments and blocked comments per day. The request must include the
            'date_from' and 'date_to' query parameters in the format YYYY-MM-DD."""
    ),
    parameters=[
        OpenApiParameter(
            name="date_from",
            description="The start date of the range (inclusive) in YYYY-MM-DD format.",
            required=True,
            type=str,
        ),
        OpenApiParameter(
            name="date_to",
            description="The end date of the range (inclusive) in YYYY-MM-DD format.",
            required=True,
            type=str,
        ),
    ],
    responses={
        200: OpenApiExample(
            "Successful response",
            value=[
                {
                    "date": "2024-02-02",
                    "total_comments": 12,
                    "blocked_comments": 3,
                },
                {
                    "date": "2024-02-03",
                    "total_comments": 5,
                    "blocked_comments": 0,
                },
            ],
            response_only=True,
        ),
        400: OpenApiExample(
            "Bad request due to missing or invalid date parameters",
            value={"error": "Please provide both 'date_from' and 'date_to' query parameters."},
            response_only=True,
        ),
    }
)
class CommentsDailyBreakdown(APIView):
    """
    API View to get the daily breakdown of comments, including total comments and blocked comments per day.
    """
    pagination_class = PageNumberPagination

    def get(self, request):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')

        if not date_from or not date_to:
            return Response({"error": "Please provide both 'date_from' and 'date_to' query parameters."}, status=400)

        date_from = parse_date(date_from)
        date_to = parse_date(date_to)

        if not date_from or not date_to:
            return Response({"error": "Invalid date format. Please use YYYY-MM-DD."}, status=400)

        comments_data = (
            Comment.objects.filter(created_at__date__range=[date_from, date_to])
            .annotate(date=TruncDate('created_at'))
            .values('date')
            .annotate(
                total_comments=Count('id'),
                blocked_comments=Count('id', filter=Q(is_blocked=True))
            )
            .order_by('date')
        )

        paginator = self.pagination_class()
        paginated_data = paginator.paginate_queryset(comments_data, request)

        return paginator.get_paginated_response(paginated_data)
