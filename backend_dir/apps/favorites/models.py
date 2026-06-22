from django.db import models

from apps.accounts.models import Member
from apps.products.models import Product


class Favorite(models.Model):
    """회원이 관심 표시(찜)한 상품. 회원↔상품 다대다, 중복 방지."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="favorites"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "favorite"
        unique_together = [("member", "product")]


class VideoFavorite(models.Model):
    """회원이 찜한 YouTube 영상. 목록 표시에 필요한 정보를 캐싱해 저장한다."""

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="video_favorites"
    )
    video_id = models.CharField(max_length=20)
    title = models.CharField(max_length=300)
    thumbnail_url = models.URLField()
    channel_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "video_favorite"
        unique_together = [("member", "video_id")]
