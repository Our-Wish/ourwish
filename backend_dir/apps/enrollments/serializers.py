from rest_framework import serializers

from apps.products.models import ProductOption
from .models import Enrollment


class EnrollmentCreateSerializer(serializers.Serializer):
    """가입 요청 바디의 '형식·범위'만 검증한다.

    상품/옵션 존재 여부, 한도 초과, 중복 가입 같은 '비즈니스 규칙'은
    DB를 봐야 알 수 있으므로 View에서 처리한다.
    여기서는 "각 필드가 올바른 모양인가?"만 본다.
    """

    product_id = serializers.IntegerField(min_value=1)
    monthly_amount = serializers.IntegerField(min_value=1)
    term_months = serializers.IntegerField(min_value=1)
    intr_rate_type = serializers.ChoiceField(choices=ProductOption.IntrRateType.choices)
    rsrv_type = serializers.ChoiceField(choices=ProductOption.RsrvType.choices)
    transfer_day = serializers.IntegerField(min_value=1, max_value=31)
    enrolled_at = serializers.DateField()
    checked_condition_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        default=list,
    )


class EnrollmentResponseSerializer(serializers.ModelSerializer):
    """가입 성공(201) 응답 모양. 저장된 Enrollment 한 건을 JSON으로 변환한다."""

    enrollment_id = serializers.IntegerField(source="id", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    bank_name = serializers.CharField(source="product.bank.bank_name", read_only=True)

    class Meta:
        model = Enrollment
        fields = [
            "enrollment_id",
            "product_id",
            "product_name",
            "bank_name",
            "monthly_amount",
            "term_months",
            "transfer_day",
            "enrolled_at",
            "expected_payout_at_maturity",
            "calculated_at",
        ]
