from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet,
    CommentsDailyBreakdown,
    CommentRetrieveUpdateDestroyView,
    CommentListCreateView
)

router = DefaultRouter()
router.register(r'posts', PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='post-comments'),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view(), name='post-comment-detail'),
    path('comments-daily-breakdown/', CommentsDailyBreakdown.as_view(), name='comments-daily-breakdown'),
]
