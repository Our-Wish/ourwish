from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product, ProductOption
from apps.products.services import calculate_after_tax_payout, calculate_applied_rate
from .models import Enrollment, PaymentRecord
from .serializers import (
    EnrollmentCreateSerializer,
    EnrollmentListSerializer,
    EnrollmentResponseSerializer,
    PaymentRecordResponseSerializer,
    PaymentRecordUpdateSerializer,
)


class EnrollmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=EnrollmentListSerializer(many=True),
        summary="내 가입 상품 목록 조회 (#10)",
    )
    def get(self, request):
        # 내 가입 상품만 조회. select_related로 product·bank를 JOIN해 한 번에 가져온다
        # (목록 직렬화 때 product_name·bank_name을 꺼내며 쿼리가 추가로 안 나가게).
        enrollments = (
            Enrollment.objects.filter(member=request.user)
            .select_related("product", "product__bank")
            .order_by("-enrolled_at")
        )
        serializer = EnrollmentListSerializer(enrollments, many=True)
        return Response(serializer.data)

    @extend_schema(
        request=EnrollmentCreateSerializer,
        responses={201: EnrollmentResponseSerializer},
        summary="적금 가입 (#9)",
    )
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


class EnrollmentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={204: None}, summary="가입 상품 삭제 (#11)")
    def delete(self, request, enrollment_id):
        # 1) id로 먼저 조회. 없으면 404.
        #    (member까지 같이 필터하면 '남의 것'과 '없는 것'을 구분 못 해 둘 다 404가 된다.
        #     스펙은 본인 것 아니면 403을 요구하므로 id로만 찾고 소유자는 따로 확인한다.)
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id)
        except Enrollment.DoesNotExist:
            raise NotFound("해당 가입 내역을 찾을 수 없습니다.")

        # 2) 소유자 확인. 내 것이 아니면 403.
        #    member_id는 FK의 실제 컬럼값이라 추가 쿼리 없이 비교할 수 있다.
        if enrollment.member_id != request.user.id:
            raise PermissionDenied("본인의 가입 내역만 삭제할 수 있습니다.")

        # 3) 삭제. 연결된 PaymentRecord는 모델의 on_delete=CASCADE로 함께 지워진다.
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PaymentRecordUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=PaymentRecordUpdateSerializer,
        responses={200: PaymentRecordResponseSerializer},
        summary="납입 정정 (#12)",
    )
    def patch(self, request, enrollment_id, record_id):
        # 1) URL의 enrollment_id + record_id로 납입 레코드 조회. 없으면 404.
        try:
            record = PaymentRecord.objects.select_related("enrollment").get(
                id=record_id, enrollment_id=enrollment_id
            )
        except PaymentRecord.DoesNotExist:
            raise NotFound("해당 납입 내역을 찾을 수 없습니다.")

        # 2) 소유자 확인. 내 가입의 납입이 아니면 403.
        if record.enrollment.member_id != request.user.id:
            raise PermissionDenied("본인의 납입 내역만 수정할 수 있습니다.")

        # 3) amount/status 교차검증 (월 납입액 기준값을 context로 넘김) → 저장.
        serializer = PaymentRecordUpdateSerializer(
            record,
            data=request.data,
            context={"monthly_amount": record.enrollment.monthly_amount},
        )
        serializer.is_valid(raise_exception=True)
        # 사용자가 손댄 레코드임을 표시 (자동기록과 구분).
        serializer.save(is_modified=True)

        return Response(PaymentRecordResponseSerializer(record).data)
