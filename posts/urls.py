from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, CommentsDailyBreakdown

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('comments-daily-breakdown/', CommentsDailyBreakdown.as_view(), name='comments-daily-breakdown'),
]
