from datetime import date

from rest_framework import serializers

from apps.products.models import ProductOption
from .models import Enrollment, PaymentRecord
from .utils import add_months


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


class EnrollmentListSerializer(serializers.ModelSerializer):
    """#10 내 가입 목록 한 줄의 모양. 응답(201)과 달리 maturity_date(만기일)를 넣고
    calculated_at은 빼는 등 목록 화면에 맞춰 필드를 구성한다."""

    enrollment_id = serializers.IntegerField(source="id", read_only=True)
    product_id = serializers.IntegerField(source="product.id", read_only=True)
    product_name = serializers.CharField(source="product.product_name", read_only=True)
    bank_name = serializers.CharField(source="product.bank.bank_name", read_only=True)
    maturity_date = serializers.SerializerMethodField()

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
            "maturity_date",
            "expected_payout_at_maturity",
        ]

    def get_maturity_date(self, obj) -> date:
        # DB에 없는 값이라 즉석 계산한다. enrolled_at + term_months 개월.
        return add_months(obj.enrolled_at, obj.term_months)


class PaymentRecordUpdateSerializer(serializers.ModelSerializer):
    """#12 납입 정정 요청. status에 따라 amount 규칙이 다르므로 validate에서 교차검증."""

    class Meta:
        model = PaymentRecord
        fields = ["amount", "status"]

    def validate(self, attrs):
        monthly = self.context["monthly_amount"]
        amount = attrs["amount"]
        status_value = attrs["status"]

        if status_value == PaymentRecord.Status.PAID and amount != monthly:
            raise serializers.ValidationError(
                {"amount": f"PAID는 월 납입액({monthly}원)과 같아야 합니다."}
            )
        if status_value == PaymentRecord.Status.MISSED and amount != 0:
            raise serializers.ValidationError({"amount": "MISSED는 0이어야 합니다."})
        if status_value == PaymentRecord.Status.PARTIAL and not (0 < amount < monthly):
            raise serializers.ValidationError(
                {"amount": f"PARTIAL은 0 초과 ~ 월 납입액({monthly}원) 미만이어야 합니다."}
            )
        return attrs


class PaymentRecordResponseSerializer(serializers.ModelSerializer):
    """#12 성공(200) 응답 모양."""

    record_id = serializers.IntegerField(source="id", read_only=True)
    enrollment_id = serializers.IntegerField(source="enrollment.id", read_only=True)

    class Meta:
        model = PaymentRecord
        fields = [
            "record_id",
            "enrollment_id",
            "scheduled_date",
            "amount",
            "status",
            "is_modified",
            "updated_at",
        ]
