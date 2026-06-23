from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import Member, SearchProfile


class SignupSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)
    nickname = serializers.CharField(max_length=50)

    def validate_login_id(self, value):
        if Member.objects.filter(login_id=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    def create(self, validated_data):
        validated_data["password_hash"] = make_password(validated_data.pop("password"))
        return Member.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        try:
            member = Member.objects.get(login_id=data["login_id"])
        except Member.DoesNotExist:
            raise serializers.ValidationError(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )

        if not check_password(data["password"], member.password_hash):
            raise serializers.ValidationError(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )

        data["member"] = member
        return data


class NicknameUpdateSerializer(serializers.Serializer):
    """회원 정보 수정 — 받는 값이 닉네임뿐이라 닉네임만 다룬다."""

    nickname = serializers.CharField(max_length=50)

    def validate_nickname(self, value):
        # 공백만 입력하는 경우를 막는다(CharField는 양끝 공백을 자동으로 떼지만 빈 문자열은 통과).
        value = value.strip()
        if not value:
            raise serializers.ValidationError("닉네임을 입력해 주세요.")
        return value


class SearchProfileSerializer(serializers.ModelSerializer):
    """조회/추천 프로필(STEP01+02). 회원당 1개. prefill 조회 + 저장/수정에 사용."""

    class Meta:
        model = SearchProfile
        fields = [
            "save_term",
            "monthly_amount",
            "deposit_amount",
            "birth_date",
            "salary_transfer",
            "auto_transfer",
            "card_usage",
            "housing_subscription",
            "first_transaction",
            "online_signup",
            "marketing_consent",
            "redeposit",
        ]

    def validate_monthly_amount(self, value):
        if not (50_000 <= value <= 3_000_000):
            raise serializers.ValidationError(
                "월 저축액은 5만원 이상 300만원 이하여야 합니다."
            )
        return value

    def validate_deposit_amount(self, value):
        # 예금은 거치식이라 한 번에 넣는 예치금액. 적금(5만~300만)보다 상한이 큼.
        if value is not None and not (50_000 <= value <= 50_000_000):
            raise serializers.ValidationError(
                "예치금액은 5만원 이상 5000만원 이하여야 합니다."
            )
        return value