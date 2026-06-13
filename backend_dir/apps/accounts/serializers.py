from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from .models import Member


class SignupSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)
    nickname = serializers.CharField(max_length=50)
    birth_date = serializers.DateField()
    job_status = serializers.ChoiceField(choices=Member.JobStatus.choices)
    marital_status = serializers.ChoiceField(choices=Member.MaritalStatus.choices)

    def validate_login_id(self, value):
        if Member.objects.filter(login_id=value).exists():
            raise serializers.ValidationError("이미 사용 중인 아이디입니다.")
        return value

    def create(self, validated_data):
        validated_data["password_hash"] = make_password(validated_data.pop("password"))
        return Member.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    login_id = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, data):
        try:
            member = Member.objects.get(login_id=data["login_id"])
        except Member.DoesNotExist:
            raise serializers.ValidationError(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )

        if not check_password(data["password"], member.password_hash):
            raise serializers.ValidationError(
                "아이디 또는 비밀번호가 올바르지 않습니다."
            )

        data["member"] = member
        return data
    

class MemberGoalAmountSerializer(serializers.ModelSerializer):
    member_id = serializers.IntegerField(source="id", read_only=True)
    total_goal_amount = serializers.IntegerField()

    class Meta:
        model = Member
        fields = ["member_id", "nickname", "total_goal_amount", "updated_at"]
        read_only_fields = ["nickname", "updated_at"]

    def validate_total_goal_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("total_goal_amount는 0보다 커야 합니다.")
        return value


# ---- #13 마이페이지: 응답 문서화용 직렬화기 ----
# 뷰는 계산 결과를 dict로 직접 만들어 반환하고, 이 직렬화기들은
# drf-spectacular(Swagger)가 응답 모양을 그려주도록 형태만 선언한다.
class MypageMemberSerializer(serializers.Serializer):
    nickname = serializers.CharField()
    total_goal_amount = serializers.IntegerField(allow_null=True)


class MypageSummarySerializer(serializers.Serializer):
    overall_gauge = serializers.FloatField(allow_null=True)
    total_saved_payout = serializers.IntegerField()
    enrollment_count = serializers.IntegerField()
    monthly_transfer_total = serializers.IntegerField()
    nearest_maturity_dday = serializers.IntegerField(allow_null=True)


class MypagePaymentSerializer(serializers.Serializer):
    record_id = serializers.IntegerField()
    scheduled_date = serializers.DateField()
    amount = serializers.IntegerField()
    status = serializers.CharField()
    is_modified = serializers.BooleanField()


class MypageEnrollmentSerializer(serializers.Serializer):
    enrollment_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    product_name = serializers.CharField()
    bank_name = serializers.CharField()
    monthly_amount = serializers.IntegerField()
    term_months = serializers.IntegerField()
    transfer_day = serializers.IntegerField()
    enrolled_at = serializers.DateField()
    maturity_date = serializers.DateField()
    dday = serializers.IntegerField()
    expected_payout_at_maturity = serializers.IntegerField()
    individual_gauge = serializers.FloatField()
    current_payout_estimate = serializers.IntegerField()
    paid_amount_total = serializers.IntegerField()
    recent_payments = MypagePaymentSerializer(many=True)


class MypageResponseSerializer(serializers.Serializer):
    member = MypageMemberSerializer()
    summary = MypageSummarySerializer()
    enrollments = MypageEnrollmentSerializer(many=True)