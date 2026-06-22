"""응답 형태를 Swagger 문서에 알려주기 위한 직렬화기.

DB 모델이 없는 외부 API 응답이라 ModelSerializer가 아니라 일반 Serializer를 쓴다.
실제 데이터는 youtube.py가 이미 dict로 만들어 주므로, 여기선 '문서용 명세' 역할이 크다.
"""

from rest_framework import serializers


class VideoSearchItemSerializer(serializers.Serializer):
    """검색 결과 카드 한 장에 들어갈 필드."""

    video_id = serializers.CharField()
    title = serializers.CharField()
    channel_name = serializers.CharField()
    thumbnail_url = serializers.URLField()
    published_at = serializers.DateTimeField()


class VideoDetailSerializer(serializers.Serializer):
    """영상 상세/재생 화면에 필요한 필드."""

    video_id = serializers.CharField()
    title = serializers.CharField()
    channel_name = serializers.CharField()
    published_at = serializers.DateTimeField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()
