import logging
import os
import google.generativeai as genai
from django.utils import timezone

from user.models import User
from .models import Comment
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel(os.environ["GENERATIVE_MODEL"])

logger = logging.getLogger(__name__)


def get_ai_response(comment_text):
    response = model.generate_content(f"{os.environ['PROMPT']}: {comment_text}")
    return response.text


def auto_reply_to_comment(comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        post = comment.post
        user_settings = post.author.settings

        if user_settings.auto_reply_enabled:
            ai_reply = get_ai_response(comment.content)

            if ai_reply:
                reply_content = ai_reply.strip()
                reply_author = User.objects.get(id=os.environ["AI_USER_ID"])
                Comment.objects.create(
                    post=post,
                    author=reply_author,
                    content=reply_content,
                    parent_comment=comment,
                    created_at=timezone.now(),
                    is_auto_reply=True
                )
    except Comment.DoesNotExist:
        logger.error(f"Comment with ID {comment_id} is not found.")
