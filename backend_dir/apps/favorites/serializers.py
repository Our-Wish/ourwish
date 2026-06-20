from rest_framework import serializers


class FavoriteCreateSerializer(serializers.Serializer):
    """찜 추가 요청 — product_id만."""

    product_id = serializers.IntegerField(min_value=1)
