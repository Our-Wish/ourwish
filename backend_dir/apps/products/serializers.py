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
