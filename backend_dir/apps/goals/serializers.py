from rest_framework import serializers
from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ["goal_id", "term_months", "monthly_cap", "created_at"]
        read_only_fields = ["goal_id", "created_at"]

    def validate_term_months(self, value):
        if value not in [3, 6, 12, 24, 36]:
            raise serializers.ValidationError(
                "term_months는 3, 6, 12, 24, 36 중 하나여야 합니다."
            )
        return value

    def validate_monthly_cap(self, value):
        if not (50000 <= value <= 3000000):
            raise serializers.ValidationError(
                "monthly_cap은 50000 이상 3000000 이하여야 합니다."
            )
        return value
