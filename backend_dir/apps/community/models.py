from django.db import models

from apps.accounts.models import Member


class Post(models.Model):
    """커뮤니티 게시글."""

    author = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="posts"
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "post"
        ordering = ["-created_at"]


class Comment(models.Model):
    """게시글 댓글. 게시글 1개에 댓글 여러 개(1:N)."""

    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comment"
        ordering = ["created_at"]
