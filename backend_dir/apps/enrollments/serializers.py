from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Enrollment
from .utils import calculate_achievement_gauge


class EnrollmentRegisterSerializer(serializers.Serializer):
    """상품 등록(1단계) 요청 — product_id만 받는다."""

    product_id = serializers.IntegerField(min_value=1)


class EnrollmentInfoSerializer(serializers.ModelSerializer):
    """정보 입력/수정(2단계) — 월납입·금리·시작일·만기일을 한 번에 받는다."""

    class Meta:
        model = Enrollment
        fields = ["monthly_amount", "rate", "start_date", "maturity_date"]
        extra_kwargs = {
            "monthly_amount": {"required": True, "allow_null": False},
            "rate": {"required": True, "allow_null": False},
            "start_date": {"required": True, "allow_null": False},
            "maturity_date": {"required": True, "allow_null": False},
        }

    def validate_monthly_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("월 납입액은 0보다 커야 합니다.")
        return value

    def validate_rate(self, value):
        if value < 0:
            raise serializers.ValidationError("금리는 0 이상이어야 합니다.")
        return value

    def validate(self, attrs):
        if attrs["maturity_date"] <= attrs["start_date"]:
            raise serializers.ValidationError(
                {"maturity_date": "만기일은 시작일보다 뒤여야 합니다."}
            )
        return attrs


class EnrollmentListSerializer(serializers.ModelSerializer):
    """나의 상품 관리 목록 한 줄 — 등록 상태 + (정보입력 됐으면) 달성 게이지."""

    enrollment_id = serializers.IntegerField(source="id", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    bank_name = serializers.CharField(source="product.bank.bank_name", read_only=True)
    rate = serializers.FloatField(allow_null=True)
    is_filled = serializers.SerializerMethodField()
    achievement_gauge = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            "enrollment_id",
            "product_id",
            "product_name",
            "bank_name",
            "is_filled",
            "monthly_amount",
            "rate",
            "start_date",
            "maturity_date",
            "achievement_gauge",
        ]

    def _is_filled(self, obj):
        return all(
            v is not None
            for v in (obj.monthly_amount, obj.rate, obj.start_date, obj.maturity_date)
        )

    def get_is_filled(self, obj) -> bool:
        return self._is_filled(obj)

    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_achievement_gauge(self, obj):
        # 정보입력 전이면 게이지 없음(null).
        if not self._is_filled(obj):
            return None
        return calculate_achievement_gauge(obj.start_date, obj.maturity_date)
