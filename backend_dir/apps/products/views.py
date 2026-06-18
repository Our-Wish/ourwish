from datetime import date

from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductDetailSerializer, RecommendQuerySerializer
from .services import calculate_rate_by_difficulty


# 추천 응답 한 건의 모양(문서용). 실제 값은 _build_item이 dict로 만든다.
# rate_by_difficulty = {BASE/LOW/MID/HIGH: {bonus_rate, expected_rate, expected_payout,
#                       condition_ids, summary_label}} — DictField로 단순 문서화.
RecommendItemSerializer = inline_serializer(
    name="RecommendItem",
    fields={
        "product_id": serializers.IntegerField(),
        "bank_name": serializers.CharField(),
        "bank_type": serializers.CharField(),
        "product_name": serializers.CharField(),
        "has_bonus": serializers.BooleanField(),
        "save_term": serializers.IntegerField(),
        "rsrv_type": serializers.CharField(),
        "base_rate": serializers.FloatField(),
        "max_rate": serializers.FloatField(allow_null=True),
        "rate_by_difficulty": serializers.DictField(),
    },
    many=True,
)


# Create your views here.
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: ProductDetailSerializer},
        summary="상품 상세 (#8)",
    )
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

    @extend_schema(
        parameters=[RecommendQuerySerializer],
        responses={200: RecommendItemSerializer},
        summary="추천 상품 목록 (#7) — 세후 수령액 내림차순, 페이지네이션",
    )
    def get(self, request):
        # 1) 쿼리 파라미터 검증 (term·monthly_cap 필수 / difficulty 기본 LOW)
        query = RecommendQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        term = query.validated_data["term"]
        monthly_cap = query.validated_data["monthly_cap"]
        difficulty = query.validated_data["difficulty"]

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

        # 3) 난이도로 거르지 않고 전부 포함. 상품마다 난이도별 금리를 계산하되,
        #    같은 기간의 여러 옵션 중 '선택 난이도 세후수령액'이 최대인 옵션을 대표로 쓴다.
        results = []
        for product in products:
            options = [o for o in product.options.all() if o.save_term == term]
            if not options:
                continue

            conditions = list(product.conditions.all())
            summary_labels = {
                "LOW": product.summary_label_low,
                "MID": product.summary_label_mid,
                "HIGH": product.summary_label_high,
            }

            best_item = None
            best_payout = None
            for option in options:
                rbd = calculate_rate_by_difficulty(
                    option, conditions, summary_labels, monthly_cap
                )
                payout = rbd[difficulty]["expected_payout"]
                if best_payout is None or payout > best_payout:
                    best_payout = payout
                    best_item = self._build_item(product, option, rbd)
            results.append(best_item)

        # 4) 선택 난이도의 세후 수령액 내림차순, 동률이면 product_id 오름차순
        results.sort(
            key=lambda item: (
                -item["rate_by_difficulty"][difficulty]["expected_payout"],
                item["product_id"],
            )
        )

        # 5) DRF 기본 페이지네이션으로 잘라서 응답
        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(results, request)
        return paginator.get_paginated_response(page)

    def _build_item(self, product, option, rate_by_difficulty):
        """응답 한 건(상품 1개)의 모양으로 조립."""
        return {
            "product_id": product.id,
            "bank_name": product.bank.bank_name,
            "bank_type": product.bank.bank_type,
            "product_name": product.product_name,
            "has_bonus": product.has_bonus,
            "save_term": option.save_term,
            "rsrv_type": option.rsrv_type,
            "base_rate": float(option.base_rate),
            "max_rate": float(option.max_rate) if option.max_rate is not None else None,
            "rate_by_difficulty": rate_by_difficulty,
        }
