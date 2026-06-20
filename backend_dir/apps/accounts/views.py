from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    inline_serializer,
)
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from .models import Member, SearchProfile
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    SearchProfileSerializer,
)


# Create your views here.
def get_tokens_for_member(member):
    refresh = RefreshToken()
    refresh["user_id"] = member.id
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# 로그인/회원가입 성공 응답(문서용): 토큰 + 회원 요약
AuthTokenResponseSerializer = inline_serializer(
    name="AuthTokenResponse",
    fields={
        "access": serializers.CharField(),
        "refresh": serializers.CharField(),
        "member": inline_serializer(
            name="AuthMember",
            fields={
                "id": serializers.IntegerField(),
                "login_id": serializers.CharField(),
                "nickname": serializers.CharField(),
            },
        ),
    },
)


class SignupView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=SignupSerializer,
        responses={201: AuthTokenResponseSerializer},
        summary="회원가입 + 자동 로그인 (#1)",
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
        tokens = get_tokens_for_member(member)
        return Response(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "member": {
                    "id": member.id,
                    "login_id": member.login_id,
                    "nickname": member.nickname,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: AuthTokenResponseSerializer},
        summary="로그인 (#2)",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member = serializer.validated_data["member"]
        tokens = get_tokens_for_member(member)
        return Response(
            {
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "member": {
                    "id": member.id,
                    "login_id": member.login_id,
                    "nickname": member.nickname,
                },
            }
        )


class CheckIdView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="login_id",
                type=str,
                location=OpenApiParameter.QUERY,
                required=True,
                description="중복 확인할 아이디",
            )
        ],
        responses=inline_serializer(
            name="CheckIdResponse",
            fields={"available": serializers.BooleanField()},
        ),
        summary="아이디 중복 확인 (#4)",
    )
    def get(self, request):
        login_id = request.query_params.get("login_id", "")
        if not login_id:
            return Response(
                {"detail": "login_id 파라미터가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        available = not Member.objects.filter(login_id=login_id).exists()
        return Response({"available": available})


class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=inline_serializer(
            name="TokenRefreshRequest",
            fields={"refresh": serializers.CharField()},
        ),
        responses=inline_serializer(
            name="TokenRefreshResponse",
            fields={"access": serializers.CharField()},
        ),
        summary="토큰 갱신 (#3)",
    )
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"detail": "refresh 토큰이 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            refresh = RefreshToken(refresh_token)
            return Response({"access": str(refresh.access_token)})
        except TokenError as e:
            raise InvalidToken(e.args[0])


class SearchProfileView(APIView):
    """조회/추천 프로필 — 회원당 1개. GET=prefill 조회, PUT=저장/수정."""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: SearchProfileSerializer},
        summary="조회 프로필 조회 (재방문 prefill)",
    )
    def get(self, request):
        profile = getattr(request.user, "search_profile", None)
        if profile is None:
            return Response(
                {"detail": "조회 프로필이 없습니다."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(SearchProfileSerializer(profile).data)

    @extend_schema(
        request=SearchProfileSerializer,
        responses={200: SearchProfileSerializer},
        summary="조회 프로필 저장/수정 (추천받기 제출)",
    )
    def put(self, request):
        serializer = SearchProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile, _ = SearchProfile.objects.update_or_create(
            member=request.user,
            defaults=serializer.validated_data,
        )
        return Response(SearchProfileSerializer(profile).data)
