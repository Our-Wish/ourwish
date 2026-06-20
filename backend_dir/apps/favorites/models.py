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
