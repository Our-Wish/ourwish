from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Product, PreferentialCondition
from .services import calculate_rate_by_difficulty


class RateLevelSerializer(serializers.Serializer):
    """rate_by_difficulty의 한 난이도(BASE/LOW/MID/HIGH) 모양 — Swagger 문서화 전용.

    실제 값은 services.calculate_rate_by_difficulty가 dict로 만든다.
    """

    bonus_rate = serializers.FloatField(help_text="그 난이도에서 더해지는 우대금리 합(%p)")
    expected_rate = serializers.FloatField(
        help_text="예상 적용금리 = min(base_rate + bonus_rate, max_rate)"
    )
    expected_payout = serializers.IntegerField(
        required=False, help_text="세후 수령액. 추천 목록(#7)에만 포함, 상세(#8)엔 없음"
    )
    condition_ids = serializers.ListField(
        child=serializers.IntegerField(), help_text="그 난이도에서 켜지는 우대조건 id 배열"
    )
    summary_label = serializers.CharField(
        allow_null=True, help_text="난이도 조건을 쉽게 풀어쓴 AI 요약. BASE는 항상 null"
    )


class RateByDifficultySerializer(serializers.Serializer):
    """난이도별 누적 예상금리 — BASE=기본금리, LOW·MID·HIGH는 누적(MID=LOW+MID). 문서화 전용."""

    BASE = RateLevelSerializer()
    LOW = RateLevelSerializer()
    MID = RateLevelSerializer()
    HIGH = RateLevelSerializer()


class ProductOptionDetailSerializer(serializers.Serializer):
    """#8 상세의 옵션 한 개 모양 — 문서화 전용. 실제 직렬화는 get_options가 dict로 만든다."""

    save_term = serializers.IntegerField()
    intr_rate_type = serializers.CharField()
    rsrv_type = serializers.CharField()
    base_rate = serializers.FloatField()
    max_rate = serializers.FloatField(allow_null=True)
    rate_by_difficulty = RateByDifficultySerializer()


class PreferentialConditionSerializer(serializers.ModelSerializer):
    condition_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = PreferentialCondition
        fields = ["condition_id", "label", "friendly_label", "difficulty", "rate"]


class ProductDetailSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source="id", read_only=True)
    bank_name = serializers.CharField(source="bank.bank_name", read_only=True)
    bank_type = serializers.CharField(source="bank.bank_type", read_only=True)
    base_rate = serializers.SerializerMethodField()
    max_rate = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    conditions = PreferentialConditionSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "product_id",
            "bank_name",
            "bank_type",
            "product_name",
            "join_way",
            "has_bonus",
            "base_rate",
            "max_rate",
            "join_member",
            "max_limit",
            "maturity_interest",
            "etc_note",
            "join_summary",
            "maturity_summary",
            "etc_summary",
            "options",
            "conditions",
        ]

    def _best_option(self, obj):
        options = obj.options.all()
        if not options:
            return None
        return max(options, key=lambda o: o.max_rate or o.base_rate)

    def get_base_rate(self, obj) -> float:
        best = self._best_option(obj)
        return best.base_rate if best else None

    def get_max_rate(self, obj) -> float:
        best = self._best_option(obj)
        return best.max_rate if best else None

    @extend_schema_field(ProductOptionDetailSerializer(many=True))
    def get_options(self, obj):
        # 옵션마다 난이도별 누적 금리(rate_by_difficulty)를 함께 내려준다.
        # 상세 화면은 납입액이 없어 expected_payout 없이(=금리만) 계산한다.
        conditions = list(obj.conditions.all())
        summary_labels = {
            "LOW": obj.summary_label_low,
            "MID": obj.summary_label_mid,
            "HIGH": obj.summary_label_high,
        }
        return [
            {
                "save_term": option.save_term,
                "intr_rate_type": option.intr_rate_type,
                "rsrv_type": option.rsrv_type,
                "base_rate": float(option.base_rate),
                "max_rate": (
                    float(option.max_rate) if option.max_rate is not None else None
                ),
                "rate_by_difficulty": calculate_rate_by_difficulty(
                    option, conditions, summary_labels
                ),
            }
            for option in obj.options.all()
        ]


class RecommendQuerySerializer(serializers.Serializer):
    """추천 API의 쿼리 파라미터(term, monthly_cap, filter) 검증용.

    DB 모델을 만들거나 저장하는 게 아니라 '입력값 검증'만 하므로
    ModelSerializer가 아니라 일반 Serializer를 쓴다.
    """

    term = serializers.ChoiceField(choices=[3, 6, 12, 24, 36])
    monthly_cap = serializers.IntegerField(min_value=1)
    # 정렬 기준 난이도. 응답엔 BASE/LOW/MID/HIGH 모두 담고, 이 값의 세후수령액으로 정렬한다.
    # BASE = 우대조건 하나도 안 챙긴 기본금리.
    difficulty = serializers.ChoiceField(
        choices=["BASE", "LOW", "MID", "HIGH"], default="BASE"
    )
