from rest_framework import serializers

from .models import Product, ProductOption, PreferentialCondition


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
    options = ProductOptionSerializer(many=True, read_only=True)
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

    def get_base_rate(self, obj):
        best = self._best_option(obj)
        return best.base_rate if best else None

    def get_max_rate(self, obj):
        best = self._best_option(obj)
        return best.max_rate if best else None


class RecommendQuerySerializer(serializers.Serializer):
    """추천 API의 쿼리 파라미터(term, monthly_cap, filter) 검증용.

    DB 모델을 만들거나 저장하는 게 아니라 '입력값 검증'만 하므로
    ModelSerializer가 아니라 일반 Serializer를 쓴다.
    """

    term = serializers.ChoiceField(choices=[3, 6, 12, 24, 36])
    monthly_cap = serializers.IntegerField(min_value=1)
    filter = serializers.ChoiceField(
        choices=["base", "low", "mid", "high"], default="base"
    )
