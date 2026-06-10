from datetime import date

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, PreferentialCondition
from .serializers import (
    ProductDetailSerializer,
    PreferentialConditionSerializer,
    RecommendQuerySerializer,
)
from .services import calculate_after_tax_payout


# 난이도 비교용 순위: 숫자가 클수록 어렵다. difficulty가 None이면 가장 어려운 것으로 취급(3).
DIFFICULTY_RANK = {
    PreferentialCondition.Difficulty.LOW: 1,
    PreferentialCondition.Difficulty.MID: 2,
    PreferentialCondition.Difficulty.HIGH: 3,
}


# Create your views here.
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("bank").prefetch_related(
                "options", "conditions"
            ),
            id=product_id,
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1) 쿼리 파라미터 검증 (term·monthly_cap 필수 / filter 기본 base)
        query = RecommendQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        term = query.validated_data["term"]
        monthly_cap = query.validated_data["monthly_cap"]
        filter_value = query.validated_data["filter"]

        # 2) 공시 종료된 상품 제외 + 연관 데이터(은행/옵션/조건)까지 한 번에 조회
        today = date.today().strftime("%Y%m%d")
        products = (
            Product.objects.select_related("bank")
            .prefetch_related("options", "conditions")
            .filter(
                Q(dcls_end_day__isnull=True)
                | Q(dcls_end_day="")
                | Q(dcls_end_day__gte=today)
            )
        )

        # 3) 상품별로 (해당 기간의) 최선 옵션과 세후 수령액 계산 + 필터 통과분만 수집
        results = []
        for product in products:
            options = [o for o in product.options.all() if o.save_term == term]
            if not options:
                continue
            if not self._passes_filter(product, filter_value):
                continue

            best_option, payout = max(
                (
                    (
                        option,
                        calculate_after_tax_payout(
                            monthly_cap, term, option.base_rate, option.intr_rate_type
                        ),
                    )
                    for option in options
                ),
                key=lambda pair: pair[1],
            )
            results.append(self._build_item(product, best_option, payout))

        # 4) 세후 수령액 내림차순, 동률이면 product_id 오름차순
        results.sort(key=lambda item: (-item["expected_payout"], item["product_id"]))

        # 5) DRF 기본 페이지네이션으로 잘라서 응답
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(results, request)
        return paginator.get_paginated_response(page)

    def _passes_filter(self, product, filter_value):
        """filter 값에 따라 이 상품을 추천 목록에 포함할지 여부를 반환."""
        if filter_value == "base":
            return not product.has_bonus
        if filter_value == "high":
            return True
        # low / mid: 기본금리 상품은 항상 포함 + 우대상품은 '최고 난이도'가 기준 이하일 때만
        if not product.has_bonus:
            return True
        threshold = 1 if filter_value == "low" else 2  # low→LOW(1)까지, mid→MID(2)까지
        max_rank = max(
            (DIFFICULTY_RANK.get(c.difficulty, 3) for c in product.conditions.all()),
            default=1,
        )
        return max_rank <= threshold

    def _build_item(self, product, option, payout):
        """응답 한 건(상품 1개)의 모양으로 조립."""
        return {
            "product_id": product.id,
            "bank_name": product.bank.bank_name,
            "bank_type": product.bank.bank_type,
            "product_name": product.product_name,
            "has_bonus": product.has_bonus,
            "base_rate": float(option.base_rate),
            "max_rate": float(option.max_rate) if option.max_rate is not None else None,
            "save_term": option.save_term,
            "rsrv_type": option.rsrv_type,
            "expected_payout": payout,
            "conditions": PreferentialConditionSerializer(
                product.conditions.all(), many=True
            ).data,
        }
