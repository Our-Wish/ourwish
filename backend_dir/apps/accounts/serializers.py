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