from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime

from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Comment, Post

from user.models import User


class CommentsDailyBreakdownTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            password='testpassword',
            is_staff=True
        )
        self.client.login(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user).access_token

        post = Post.objects.create(
            title='title',
            content='content',
            created_at=datetime(2023, 10, 15),
            author=self.user,
            is_blocked=False)
        Comment.objects.create(
            content="First comment",
            created_at=datetime(2023, 10, 15),
            is_blocked=False,
            author=self.user,
            post_id=post.id
        )
        Comment.objects.create(
            content="Second comment",
            created_at=datetime(2023, 10, 16),
            is_blocked=True,
            author=self.user,
            post_id=post.id
        )
        Comment.objects.create(
            content="Third comment",
            created_at=datetime(2023, 10, 17),
            is_blocked=False,
            author=self.user,
            post_id=post.id
        )

    def test_comments_daily_breakdown_success(self):
        url = reverse('posts:comments-daily-breakdown')
        response = self.client.get(
            url,
            {'date_from': '2000-01-01', 'date_to': '2055-01-01'},
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['total_comments'], 3)
        self.assertEqual(response.data['results'][0]['blocked_comments'], 1)

    def test_comments_daily_breakdown_missing_dates(self):
        url = reverse('posts:comments-daily-breakdown')
        response = self.client.get(
            url,
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Please provide both 'date_from' and 'date_to' query parameters.")

    def test_comments_daily_breakdown_invalid_dates(self):
        url = reverse('posts:comments-daily-breakdown')
        response = self.client.get(
            url,
            {'date_from': 'invalid-date', 'date_to': 'invalid-date'},
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Invalid date format. Please use YYYY-MM-DD.")


class CreatePostTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.token = RefreshToken.for_user(self.user).access_token

    def test_create_post_success(self):
        url = reverse('posts:post-list')
        data = {
            'title': 'Valid Title',
            'content': 'This is a valid content without profanity.',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, 'Valid Title')
        self.assertFalse(Post.objects.get().is_blocked)

    def test_create_post_with_profanity(self):
        url = reverse('posts:post-list')
        data = {
            'title': 'Bad Title with profanity',
            'content': 'This content has a bad word: SHIT!'
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertTrue(Post.objects.get().is_blocked)

    def test_update_post_success(self):
        post = Post.objects.create(
            title='title',
            content='content',
            created_at=datetime(2023, 10, 15),
            author=self.user,
            is_blocked=False
        )
        url = reverse('posts:post-detail', kwargs={'pk': post.pk})
        data = {
            'title': 'New Valid Title',
            'content': 'This is an updated valid content.'
        }
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(post.title, 'New Valid Title')
        self.assertFalse(post.is_blocked)

    def test_update_post_with_profanity(self):
        post = Post.objects.create(
            title='title',
            content='content',
            created_at=datetime(2023, 10, 15),
            author=self.user,
            is_blocked=False
        )
        url = reverse('posts:post-detail', kwargs={'pk': post.pk})
        data = {
            'title': 'Updated Title with profanity',
            'content': 'This content contains a bad word: SHIT!'
        }

        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        post.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(post.is_blocked)
