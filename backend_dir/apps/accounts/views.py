from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken


from .models import Member
from .serializers import SignupSerializer, LoginSerializer


# Create your views here.
def get_tokens_for_member(member):
    refresh = RefreshToken()
    refresh["user_id"] = member.id
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class SignupView(APIView):
    permission_classes = [AllowAny]

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
