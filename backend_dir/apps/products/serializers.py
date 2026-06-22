from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Product, ProductOption


class ProductOptionSerializer(serializers.ModelSerializer):
    """상세의 옵션 한 개 — save_term·금리타입·base/max만(난이도 계산 제거)."""

    base_rate = serializers.FloatField()
    max_rate = serializers.FloatField(allow_null=True)

    class Meta:
        model = ProductOption
        fields = ["save_term", "intr_rate_type", "rsrv_type", "base_rate", "max_rate"]


class ProductTagSerializer(serializers.Serializer):
    """상품이 제공하는 매칭 태그 4개(문서화용)."""

    salary_transfer = serializers.BooleanField()
    auto_transfer = serializers.BooleanField()
    card_usage = serializers.BooleanField()
    housing_subscription = serializers.BooleanField()


class ProductDetailSerializer(serializers.ModelSerializer):
    """#8 상품 상세. FSS 원문 필드 + 우대조건 전문 + AI 요약 + 태그/연령."""

    product_id = serializers.IntegerField(source="id", read_only=True)
    bank_name = serializers.CharField(source="bank.bank_name", read_only=True)
    bank_type = serializers.CharField(source="bank.bank_type", read_only=True)
    product_type = serializers.CharField(read_only=True)  # "SAVINGS"(적금) / "DEPOSIT"(예금)
    base_rate = serializers.SerializerMethodField()
    max_rate = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    options = ProductOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "bank_name",
            "bank_type",
            "product_type",
            "product_name",
            # FSS 원문 5필드(문자열 그대로 노출)
            "join_member",
            "join_way",
            "max_limit",
            "maturity_interest",
            "etc_note",
            "special_condition_raw",  # 우대조건 전문(파싱 없이)
            "ai_summary",
            "tags",
            "age_min",
            "age_max",
            "is_favorited",
            "base_rate",
            "max_rate",
            "options",
        ]

    def _best_option(self, obj):
        options = obj.options.all()
        if not options:
            return None
        return max(options, key=lambda o: o.max_rate or o.base_rate)

    def get_base_rate(self, obj) -> float:
        best = self._best_option(obj)
        return float(best.base_rate) if best else None

    def get_max_rate(self, obj) -> float:
        best = self._best_option(obj)
        if best and best.max_rate is not None:
            return float(best.max_rate)
        return None

    @extend_schema_field(ProductTagSerializer)
    def get_tags(self, obj):
        return {
            "salary_transfer": obj.tag_salary_transfer,
            "auto_transfer": obj.tag_auto_transfer,
            "card_usage": obj.tag_card_usage,
            "housing_subscription": obj.tag_housing_subscription,
        }

    @extend_schema_field(serializers.BooleanField())
    def get_is_favorited(self, obj):
        # 뷰가 context로 넣어준 현재 유저의 찜 여부(하트 채움 표시용).
        return self.context.get("is_favorited", False)


class RecommendQuerySerializer(serializers.Serializer):
    """추천 목록 정렬 기준(쿼리 파라미터).

    base = 기본금리로 계산한 세후수령액순, max = 최고금리로 계산한 수령액순,
    all  = 내가 고른 우대조건을 전부 만족(AND)하는 상품만 추려 최고금리 수령액순.
    """

    sort = serializers.ChoiceField(choices=["base", "max", "all"], default="base")
    # 적금(SAVINGS, 기본값) / 예금(DEPOSIT) — 추천 대상 상품군 선택.
    product_type = serializers.ChoiceField(
        choices=["SAVINGS", "DEPOSIT"], default="SAVINGS"
    )
