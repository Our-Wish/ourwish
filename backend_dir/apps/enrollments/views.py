from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, ProductOption
from apps.products.services import calculate_after_tax_payout, calculate_applied_rate
from .models import Enrollment
from .serializers import EnrollmentCreateSerializer, EnrollmentResponseSerializer


class EnrollmentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1) 입력 형식 검증 (실패 시 자동 400)
        serializer = EnrollmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        # 2) 상품 존재 확인 (없으면 404)
        try:
            product = Product.objects.select_related("bank").get(id=data["product_id"])
        except Product.DoesNotExist:
            raise NotFound("해당 상품을 찾을 수 없습니다.")

        # 3) 옵션(기간·단복리·정액자유 조합) 존재 확인 (없으면 404)
        try:
            option = product.options.get(
                save_term=data["term_months"],
                intr_rate_type=data["intr_rate_type"],
                rsrv_type=data["rsrv_type"],
            )
        except ProductOption.DoesNotExist:
            raise NotFound("선택한 조건에 맞는 상품 옵션이 없습니다.")

        # 4) 월 납입액이 상품 한도 이내인지 (초과면 400)
        if product.max_limit is not None and data["monthly_amount"] > product.max_limit:
            raise ValidationError(
                {
                    "monthly_amount": f"이 상품의 최대 납입 한도({product.max_limit}원)를 초과했습니다."
                }
            )

        # 5) 체크한 우대조건이 모두 이 상품 것인지 (아니면 400) + rate 수집
        checked_ids = data["checked_condition_ids"]
        conditions = list(product.conditions.filter(id__in=checked_ids))
        if len(conditions) != len(set(checked_ids)):
            raise ValidationError(
                {"checked_condition_ids": "이 상품에 속하지 않는 우대조건이 포함되어 있습니다."}
            )

        # 6) 이미 가입한 상품인지 (중복이면 409)
        if Enrollment.objects.filter(member=request.user, product=product).exists():
            return Response(
                {"detail": "이미 가입한 상품입니다."},
                status=status.HTTP_409_CONFLICT,
            )

        # 7) 적용금리(기본+우대, max_rate cap) → 만기 세후 수령액 계산
        applied_rate = calculate_applied_rate(
            option.base_rate, option.max_rate, [c.rate for c in conditions]
        )
        payout = calculate_after_tax_payout(
            data["monthly_amount"],
            data["term_months"],
            applied_rate,
            data["intr_rate_type"],
        )

        # 8) Enrollment 저장 (expected_payout_at_maturity 박제)
        enrollment = Enrollment.objects.create(
            member=request.user,
            product=product,
            monthly_amount=data["monthly_amount"],
            term_months=data["term_months"],
            expected_payout_at_maturity=payout,
            transfer_day=data["transfer_day"],
            enrolled_at=data["enrolled_at"],
        )

        # 9) 201 응답
        return Response(
            EnrollmentResponseSerializer(enrollment).data,
            status=status.HTTP_201_CREATED,
        )
