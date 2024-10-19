from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    auto_reply_enabled = models.BooleanField(default=False)
    auto_reply_delay = models.IntegerField(default=10)

    def __str__(self):
        return f"Settings for {self.user.email}"
