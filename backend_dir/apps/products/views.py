from datetime import date

from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.favorites.models import Favorite
from .models import Product
from .serializers import ProductDetailSerializer, RecommendQuerySerializer
from .services import calculate_after_tax_payout

# 유저 프로필(SearchProfile)의 우대조건 플래그 ↔ 상품 태그 필드 매핑.
_TAG_FIELDS = ["salary_transfer", "auto_transfer", "card_usage", "housing_subscription"]


# 추천 응답 한 건의 모양(문서용). 실제 값은 _build_item이 dict로 만든다.
RecommendItemSerializer = inline_serializer(
    name="RecommendItem",
    fields={
        "product_id": serializers.IntegerField(),
        "bank_name": serializers.CharField(),
        "bank_type": serializers.CharField(),
        "product_name": serializers.CharField(),
        "save_term": serializers.IntegerField(),
        "base_rate": serializers.FloatField(),
        "max_rate": serializers.FloatField(allow_null=True),
        "expected_payout": serializers.IntegerField(),
        "matched_tags": serializers.ListField(child=serializers.CharField()),
    },
    many=True,
)


def _calc_age(birth_date):
    """생년월일 → 만 나이."""
    today = date.today()
    return (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )


def _age_ok(age, age_min, age_max):
    """상품의 연령 제한(없으면 None)에 유저 나이가 들어맞는지."""
    if age_min is not None and age < age_min:
        return False
    if age_max is not None and age > age_max:
        return False
    return True


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: ProductDetailSerializer},
        summary="상품 상세 (#8)",
    )
    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("bank").prefetch_related("options"),
            id=product_id,
        )
        is_favorited = Favorite.objects.filter(
            member=request.user, product=product
        ).exists()
        serializer = ProductDetailSerializer(
            product, context={"is_favorited": is_favorited}
        )
        return Response(serializer.data)


class ProductRecommendView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[RecommendQuerySerializer],
        responses={200: RecommendItemSerializer},
        summary="추천 상품 목록 (#7) — 저장된 조회 프로필 기반, 세후 수령액 내림차순",
    )
    def get(self, request):
        query = RecommendQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        sort = query.validated_data["sort"]

        # 저장된 조회 프로필을 읽어 필터 재료로 쓴다. 없으면 추천 불가.
        profile = getattr(request.user, "search_profile", None)
        if profile is None:
            return Response(
                {"detail": "조회 프로필을 먼저 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        term = profile.save_term
        monthly = profile.monthly_amount
        age = _calc_age(profile.birth_date)
        # 유저가 T로 답한 우대조건 태그 목록.
        wanted = [tag for tag in _TAG_FIELDS if getattr(profile, tag)]
        use_max = sort in ("max", "all")  # base만 기본금리, 나머지는 최고금리

        today = date.today().strftime("%Y%m%d")
        products = (
            Product.objects.select_related("bank")
            .prefetch_related("options")
            .filter(
                Q(dcls_end_day__isnull=True)
                | Q(dcls_end_day="")
                | Q(dcls_end_day__gte=today)
            )
        )

        results = []
        for product in products:
            # 1) 기간 필터: 해당 save_term 옵션이 있어야 함
            options = [o for o in product.options.all() if o.save_term == term]
            if not options:
                continue
            # 2) 월 납입 한도 필터
            if product.max_limit is not None and monthly > product.max_limit:
                continue
            # 3) 연령 필터
            if not _age_ok(age, product.age_min, product.age_max):
                continue
            # 4) 우대조건 태그 매칭 (T로 답한 게 있을 때만)
            matched = [t for t in wanted if getattr(product, f"tag_{t}")]
            if wanted:
                if sort == "all" and len(matched) < len(wanted):
                    continue  # AND: 전부 만족해야 통과
                if sort != "all" and not matched:
                    continue  # OR: 하나라도 만족

            # 대표 옵션 = 선택 금리 기준 세후수령액이 가장 큰 옵션
            best_option = None
            best_payout = None
            for option in options:
                rate = (
                    option.max_rate
                    if use_max and option.max_rate is not None
                    else option.base_rate
                )
                payout = calculate_after_tax_payout(
                    monthly, term, rate, option.intr_rate_type
                )
                if best_payout is None or payout > best_payout:
                    best_payout = payout
                    best_option = option

            results.append(
                self._build_item(product, best_option, best_payout, matched)
            )

        # 세후 수령액 내림차순, 동률이면 product_id 오름차순
        results.sort(key=lambda item: (-item["expected_payout"], item["product_id"]))

        paginator = PageNumberPagination()
        page = paginator.paginate_queryset(results, request)
        return paginator.get_paginated_response(page)

    def _build_item(self, product, option, expected_payout, matched_tags):
        return {
            "product_id": product.id,
            "bank_name": product.bank.bank_name,
            "bank_type": product.bank.bank_type,
            "product_name": product.product_name,
            "save_term": option.save_term,
            "base_rate": float(option.base_rate),
            "max_rate": (
                float(option.max_rate) if option.max_rate is not None else None
            ),
            "expected_payout": expected_payout,
            "matched_tags": matched_tags,
        }
