from datetime import date

from django.db.models import Q
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.favorites.models import Favorite
from .llm import stream_chat_reply
from .models import Product
from .serializers import ProductDetailSerializer, RecommendQuerySerializer
from .services import calculate_after_tax_payout, calculate_deposit_after_tax_payout

# 유저 프로필(SearchProfile)의 우대조건 플래그 ↔ 상품 태그 필드 매핑.
# 상품군(product_type)마다 STEP02 질문이 달라 태그 집합도 다르다.
#   적금: 급여이체·자동이체·카드실적·청약
#   예금: 첫거래·비대면가입·마케팅동의·재예치 (예금 우대조건 데이터 빈도 기준)
_SAVINGS_TAG_FIELDS = ["salary_transfer", "auto_transfer", "card_usage", "housing_subscription"]
_DEPOSIT_TAG_FIELDS = ["first_transaction", "online_signup", "marketing_consent", "redeposit"]

# 우대조건 원문이 사실상 비어있음을 뜻하는 값들(파싱 없이 단순 판정).
# 예금 데이터에 '해당사항없음'·'우대조건없음'류가 많아 함께 포함한다.
_NO_CONDITION = {"", "없음", "해당없음", "해당사항없음", "우대조건없음", "우대사항없음"}


def _has_conditions(raw):
    """우대조건 원문에 실제 내용이 있으면 True. 비어있거나 '없음'류면 False."""
    # 공백 제거 후 비교 → "해당사항 없음" 같은 띄어쓰기 변형도 함께 잡는다.
    return (raw or "").replace(" ", "").strip() not in _NO_CONDITION


# 추천 응답 한 건의 모양(문서용). 실제 값은 _build_item이 dict로 만든다.
RecommendItemSerializer = inline_serializer(
    name="RecommendItem",
    fields={
        "product_id": serializers.IntegerField(),
        "bank_name": serializers.CharField(),
        "bank_type": serializers.CharField(),
        "product_type": serializers.CharField(),
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
        product_type = query.validated_data["product_type"]
        is_deposit = product_type == Product.ProductType.DEPOSIT

        # 저장된 조회 프로필을 읽어 필터 재료로 쓴다. 없으면 추천 불가.
        profile = getattr(request.user, "search_profile", None)
        if profile is None:
            return Response(
                {"detail": "조회 프로필을 먼저 입력해주세요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        term = profile.save_term
        # 적금=월 납입액으로, 예금=한 번에 넣는 예치금액으로 추천 계산을 한다.
        if is_deposit:
            amount = profile.deposit_amount
            if amount is None:
                return Response(
                    {"detail": "예치금액을 먼저 입력해주세요."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            amount = profile.monthly_amount
        age = _calc_age(profile.birth_date)
        # 상품군에 맞는 태그 집합에서, 유저가 T로 답한 것만 추린다.
        tag_fields = _DEPOSIT_TAG_FIELDS if is_deposit else _SAVINGS_TAG_FIELDS
        wanted = [tag for tag in tag_fields if getattr(profile, tag)]
        use_max = sort in ("max", "all")  # base만 기본금리, 나머지는 최고금리

        today = date.today().strftime("%Y%m%d")
        products = (
            Product.objects.select_related("bank")
            .prefetch_related("options")
            .filter(product_type=product_type)
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
            # 2) 한도 필터 (적금=월 납입 한도, 예금=가입 한도)
            if product.max_limit is not None and amount > product.max_limit:
                continue
            # 2-1) 최소금액 필터 — 내 금액이 상품 최소가입금액에 못 미치면 제외
            if product.min_limit is not None and amount < product.min_limit:
                continue
            # 3) 연령 필터
            if not _age_ok(age, product.age_min, product.age_max):
                continue
            # 4) 우대조건 태그 매칭 (T로 답한 게 있을 때만)
            matched = [t for t in wanted if getattr(product, f"tag_{t}")]
            if wanted:
                if sort == "all":
                    # AND: 내가 고른 조건을 전부 만족해야 통과(무조건 상품도 제외됨)
                    if len(matched) < len(wanted):
                        continue
                else:
                    # OR: 매칭되거나, 우대조건이 아예 없는 상품(충족할 게 없어 누구에게나
                    # 공정)이면 통과. "조건은 있는데 내 태그로 안 잡히는 상품"만 제외.
                    if not matched and _has_conditions(product.special_condition_raw):
                        continue

            # 대표 옵션 = 선택 금리 기준 세후수령액이 가장 큰 옵션
            best_option = None
            best_payout = None
            for option in options:
                rate = (
                    option.max_rate
                    if use_max and option.max_rate is not None
                    else option.base_rate
                )
                if is_deposit:
                    payout = calculate_deposit_after_tax_payout(
                        amount, term, rate, option.intr_rate_type
                    )
                else:
                    payout = calculate_after_tax_payout(
                        amount, term, rate, option.intr_rate_type
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
            "product_type": product.product_type,
            "product_name": product.product_name,
            "save_term": option.save_term,
            "base_rate": float(option.base_rate),
            "max_rate": (
                float(option.max_rate) if option.max_rate is not None else None
            ),
            "expected_payout": expected_payout,
            "matched_tags": matched_tags,
        }


class ProductChatView(APIView):
    """상품 상세 AI 챗봇 — 대화를 받아 GMS 답변을 '스트리밍'으로 흘려보낸다.

    대화는 프론트가 보관(백엔드 stateless). body 예: {"messages": [{role, content}, ...]}.
    응답은 JSON이 아니라 text/plain '스트림'(답변 조각이 실시간으로 흘러나옴).
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=inline_serializer(
            name="ChatRequest",
            fields={"messages": serializers.ListField(child=serializers.DictField())},
        ),
        summary="상품 상세 AI 챗봇 (스트리밍, #108)",
        description="대화 배열을 받아 GMS 답변을 text/plain 스트림으로 반환.",
    )
    def post(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("bank"), id=product_id
        )

        messages = request.data.get("messages")
        # 내용 있는 user 질문이 하나라도 있어야 함(없으면 스트림 열기 전에 400).
        has_question = isinstance(messages, list) and any(
            isinstance(m, dict)
            and m.get("role") == "user"
            and (m.get("content") or "").strip()
            for m in messages
        )
        if not has_question:
            return Response(
                {"detail": "messages 배열에 user 질문이 필요해요."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 제너레이터를 그대로 넘기면, 답변 조각이 생기는 대로 클라이언트로 흘러나간다.
        response = StreamingHttpResponse(
            stream_chat_reply(product, messages),
            content_type="text/plain; charset=utf-8",
        )
        # nginx가 응답을 모아뒀다 한꺼번에 주지 않도록(=실시간 스트리밍) 끄는 헤더.
        response["X-Accel-Buffering"] = "no"
        response["Cache-Control"] = "no-cache"
        return response
