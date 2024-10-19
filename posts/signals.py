import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment
from .tasks import auto_reply_to_comment


@receiver(post_save, sender=Comment)
def comment_post_save(sender, instance, created, **kwargs):
    if created and not instance.is_auto_reply:
        user_settings = instance.post.author.settings
        if user_settings.auto_reply_enabled:
            delay = user_settings.auto_reply_delay
            timer = threading.Timer(delay, auto_reply_to_comment, args=(instance.id,))
            timer.start()
