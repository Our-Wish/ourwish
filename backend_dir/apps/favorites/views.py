from drf_spectacular.utils import OpenApiParameter, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from apps.products.services import (
    calculate_after_tax_payout,
    calculate_deposit_after_tax_payout,
)
from .models import Favorite
from .serializers import FavoriteCreateSerializer

# 찜 목록 한 건의 모양(문서용) — 추천 카드와 동일.
FavoriteItemSerializer = inline_serializer(
    name="FavoriteItem",
    fields={
        "product_id": serializers.IntegerField(),
        "bank_name": serializers.CharField(),
        "bank_type": serializers.CharField(),
        "product_type": serializers.CharField(),
        "product_name": serializers.CharField(),
        "base_rate": serializers.FloatField(allow_null=True),
        "max_rate": serializers.FloatField(allow_null=True),
        "expected_payout": serializers.IntegerField(allow_null=True),
    },
    many=True,
)

FavoriteCreatedSerializer = inline_serializer(
    name="FavoriteCreated",
    fields={
        "detail": serializers.CharField(),
        "product_id": serializers.IntegerField(),
    },
)


def _best_by_rate(product):
    """금리(최고>기본) 가장 높은 옵션. 프로필 없을 때 base/max 표시용."""
    options = list(product.options.all())
    if not options:
        return None
    return max(options, key=lambda o: o.max_rate or o.base_rate)


def _best_by_payout(product, amount, use_max, is_deposit):
    """선택 금리 기준 세후수령액이 가장 큰 옵션 → (option, payout).

    적금=적립식·월납입(amount=월저축액), 예금=거치식·목돈 일시(amount=예치금액).
    """
    best = None
    for option in product.options.all():
        rate = (
            option.max_rate
            if use_max and option.max_rate is not None
            else option.base_rate
        )
        if is_deposit:
            payout = calculate_deposit_after_tax_payout(
                amount, option.save_term, rate, option.intr_rate_type
            )
        else:
            payout = calculate_after_tax_payout(
                amount, option.save_term, rate, option.intr_rate_type
            )
        if best is None or payout > best[1]:
            best = (option, payout)
    return best


class FavoriteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="sort",
                type=str,
                location=OpenApiParameter.QUERY,
                description="수령액 계산 기준 금리: base(기본·기본값) | max(최고)",
            )
        ],
        responses={200: FavoriteItemSerializer},
        summary="내 찜 목록",
    )
    def get(self, request):
        use_max = request.query_params.get("sort") == "max"
        profile = getattr(request.user, "search_profile", None)

        favorites = (
            Favorite.objects.filter(member=request.user)
            .select_related("product", "product__bank")
            .prefetch_related("product__options")
            .order_by("-created_at")
        )

        items = []
        for fav in favorites:
            product = fav.product
            is_deposit = product.product_type == Product.ProductType.DEPOSIT
            # 금리(base/max)는 항상 상품의 대표(최고금리) 옵션에서 — 카드 헤드라인용.
            headline = _best_by_rate(product)
            base_rate = float(headline.base_rate) if headline else None
            max_rate = (
                float(headline.max_rate)
                if headline and headline.max_rate is not None
                else None
            )
            # 예상 수령액은 프로필에 해당 금액이 있을 때만. 적금=월저축액, 예금=예치금액.
            expected_payout = None
            if profile is not None:
                amount = (
                    profile.deposit_amount if is_deposit else profile.monthly_amount
                )
                if amount is not None:
                    best = _best_by_payout(product, amount, use_max, is_deposit)
                    if best is not None:
                        expected_payout = best[1]
            items.append(
                {
                    "product_id": product.id,
                    "bank_name": product.bank.bank_name,
                    "bank_type": product.bank.bank_type,
                    "product_type": product.product_type,
                    "product_name": product.product_name,
                    "base_rate": base_rate,
                    "max_rate": max_rate,
                    "expected_payout": expected_payout,
                }
            )
        return Response(items)

    @extend_schema(
        request=FavoriteCreateSerializer,
        responses={201: FavoriteCreatedSerializer},
        summary="찜 추가 (이미 찜했으면 그대로 유지)",
    )
    def post(self, request):
        serializer = FavoriteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            product = Product.objects.get(id=serializer.validated_data["product_id"])
        except Product.DoesNotExist:
            raise NotFound("해당 상품을 찾을 수 없습니다.")

        Favorite.objects.get_or_create(member=request.user, product=product)
        return Response(
            {"detail": "찜에 추가했습니다.", "product_id": product.id},
            status=status.HTTP_201_CREATED,
        )


class FavoriteDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={204: None}, summary="찜 해제")
    def delete(self, request, product_id):
        deleted, _ = Favorite.objects.filter(
            member=request.user, product_id=product_id
        ).delete()
        if not deleted:
            raise NotFound("찜한 상품이 아닙니다.")
        return Response(status=status.HTTP_204_NO_CONTENT)
