from rest_framework import serializers

from .models import Product, ProductOption, PreferentialCondition
from .services import calculate_rate_by_difficulty


class ProductOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOption
        fields = ["save_term", "intr_rate_type", "rsrv_type", "base_rate", "max_rate"]


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
