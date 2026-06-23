from rest_framework import serializers

from .models import VideoFavorite


class FavoriteCreateSerializer(serializers.Serializer):
    """찜 추가 요청 — product_id만."""

    product_id = serializers.IntegerField(min_value=1)


class VideoFavoriteSerializer(serializers.ModelSerializer):
    """영상 찜 — 목록 표시에 필요한 정보를 통째로 저장한다(YouTube는 DB에 없으므로 캐싱).

    POST 요청 본문(등록)과 GET 목록 응답을 겸한다.
    """

    class Meta:
        model = VideoFavorite
        fields = ["video_id", "title", "thumbnail_url", "channel_name", "created_at"]
        # created_at은 응답에만 나가고, 등록 시엔 서버가 자동으로 채운다.
        read_only_fields = ["created_at"]
