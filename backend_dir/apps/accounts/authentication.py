from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Member


class MemberJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            member_id = validated_token["user_id"]
        except KeyError:
            raise InvalidToken("Token contained no recognizable user identification")

        try:
            return Member.objects.get(id=member_id)
        except Member.DoesNotExist:
            raise InvalidToken("No active account found with the given credentials")
