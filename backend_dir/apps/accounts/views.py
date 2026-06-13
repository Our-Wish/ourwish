from datetime import date

from django.db.models import Prefetch, Sum
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


from apps.enrollments.models import Enrollment, PaymentRecord
from apps.enrollments.utils import add_months
from .models import Member
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    MemberGoalAmountSerializer,
    MypageResponseSerializer,
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


class MemberGoalAmountView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=MemberGoalAmountSerializer,
        responses={200: MemberGoalAmountSerializer},
        summary="최종 목표 금액 수정 (#14)",
    )
    def patch(self, request):
        serializer = MemberGoalAmountSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class MypageView(APIView):
    """#13 GET /mypage/ — 마이페이지 전체 데이터(게이지·납입현황 종합)."""

    permission_classes = [IsAuthenticated]
    RECENT_PAYMENTS_LIMIT = 3  # 가입별로 최근 납입 몇 건을 내려줄지

    @extend_schema(responses=MypageResponseSerializer)
    def get(self, request):
        member = request.user
        today = date.today()

        # 내 가입 + 상품/은행 JOIN + 납입레코드(최신순) 한 번에 로딩.
        enrollments = (
            Enrollment.objects.filter(member=member)
            .select_related("product", "product__bank")
            .prefetch_related(
                Prefetch(
                    "payment_records",
                    queryset=PaymentRecord.objects.order_by("-scheduled_date"),
                )
            )
            .order_by("-enrolled_at")
        )

        enrollment_payloads = []
        total_saved_payout = 0
        ddays = []

        for enrollment in enrollments:
            payments = list(enrollment.payment_records.all())  # 이미 최신순 정렬됨
            paid_amount_total = sum(p.amount for p in payments)
            plan_total = enrollment.monthly_amount * enrollment.term_months  # 만기까지 총 납입 예정액

            # 개별 게이지 = 납입 누계 / 만기 총 납입예정 × 100
            individual_gauge = (
                round(paid_amount_total / plan_total * 100, 1) if plan_total else 0.0
            )
            # ② 현재 세후 수령액 추정 = 박제된 만기 수령액을 납입 진척도로 안분
            current_payout_estimate = (
                round(enrollment.expected_payout_at_maturity * paid_amount_total / plan_total)
                if plan_total
                else 0
            )
            total_saved_payout += current_payout_estimate

            maturity_date = add_months(enrollment.enrolled_at, enrollment.term_months)
            dday = (maturity_date - today).days
            ddays.append(dday)

            enrollment_payloads.append(
                {
                    "enrollment_id": enrollment.id,
                    "product_id": enrollment.product_id,
                    "product_name": enrollment.product.product_name,
                    "bank_name": enrollment.product.bank.bank_name,
                    "monthly_amount": enrollment.monthly_amount,
                    "term_months": enrollment.term_months,
                    "transfer_day": enrollment.transfer_day,
                    "enrolled_at": enrollment.enrolled_at,
                    "maturity_date": maturity_date,
                    "dday": dday,
                    "expected_payout_at_maturity": enrollment.expected_payout_at_maturity,
                    "individual_gauge": individual_gauge,
                    "current_payout_estimate": current_payout_estimate,
                    "paid_amount_total": paid_amount_total,
                    "recent_payments": [
                        {
                            "record_id": p.id,
                            "scheduled_date": p.scheduled_date,
                            "amount": p.amount,
                            "status": p.status,
                            "is_modified": p.is_modified,
                        }
                        for p in payments[: self.RECENT_PAYMENTS_LIMIT]
                    ],
                }
            )

        # 이번 달 실제 납입(PAID) 합계
        monthly_transfer_total = (
            PaymentRecord.objects.filter(
                enrollment__member=member,
                status=PaymentRecord.Status.PAID,
                scheduled_date__year=today.year,
                scheduled_date__month=today.month,
            ).aggregate(total=Sum("amount"))["total"]
            or 0
        )

        # 전체 게이지: 목표금액이 없으면 null
        if member.total_goal_amount:
            overall_gauge = round(total_saved_payout / member.total_goal_amount * 100, 1)
        else:
            overall_gauge = None

        data = {
            "member": {
                "nickname": member.nickname,
                "total_goal_amount": member.total_goal_amount,
            },
            "summary": {
                "overall_gauge": overall_gauge,
                "total_saved_payout": total_saved_payout,
                "enrollment_count": len(enrollment_payloads),
                "monthly_transfer_total": monthly_transfer_total,
                "nearest_maturity_dday": min(ddays) if ddays else None,
            },
            "enrollments": enrollment_payloads,
        }
        return Response(data)
