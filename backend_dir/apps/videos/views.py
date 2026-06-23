from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import VideoDetailSerializer, VideoSearchItemSerializer
from .youtube import YouTubeError, get_video_detail, search_videos


class VideoSearchView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("q", str, description="검색어", required=True),
            OpenApiParameter("order", str, description="정렬 기준 (relevance|date|viewCount)"),
        ],
        responses=VideoSearchItemSerializer(many=True),
        summary="YouTube 영상 검색 (#149)",
    )
    def get(self, request):
        # 검색어는 필수. 공백만 들어오면 400으로 막는다.
        query = request.query_params.get("q", "").strip()
        if not query:
            raise ValidationError({"q": "검색어를 입력해 주세요."})

        order = request.query_params.get("order", "relevance")

        try:
            results = search_videos(query, order=order)
        except YouTubeError as e:
            # YouTube 쪽 실패는 우리 서버 잘못이 아니므로 502로 구분해 알린다.
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        # 결과가 없으면 빈 배열 그대로 내려준다(프론트가 '결과 없음' 안내 표시).
        return Response(results)


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=VideoDetailSerializer,
        summary="YouTube 영상 상세 (#149)",
    )
    def get(self, request, video_id):
        try:
            video = get_video_detail(video_id)
        except YouTubeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        if video is None:
            raise NotFound("해당 영상을 찾을 수 없습니다.")
        return Response(video)
