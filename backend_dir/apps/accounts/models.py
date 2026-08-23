from django.db import models


# 계정 그 자체(로그인/식별)만 담당. 추천용 입력값은 SearchProfile로 분리.
class Member(models.Model):
    login_id = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 커스텀 JWT 인증(authentication.py)이 Member를 request.user로 쓸 때 필요.
    is_authenticated = True

    class Meta:
        db_table = "member"


class SearchProfile(models.Model):
    """상품 조회/추천에 쓰는 회원 입력값. 회원당 1개(1:1).

    STEP01(기간·금액) + STEP02(나이·우대조건 4개)를 한 덩어리로 저장한다.
    처음 조회 때 생성하고, 다음 조회 땐 이 값을 prefill해 변경분만 수정한다.
    """

    class SaveTerm(models.IntegerChoices):
        M3 = 3, "3개월"
        M6 = 6, "6개월"
        M12 = 12, "12개월"
        M24 = 24, "24개월"
        M36 = 36, "36개월"

    member = models.OneToOneField(
        Member, on_delete=models.CASCADE, related_name="search_profile"
    )
    # STEP 01 — 적금(적립식)과 예금(거치식)은 기간·금액을 따로 가진다.
    # 한쪽만 쓰는 회원도 있으므로 모두 nullable. (serializer가 '기간+금액 쌍'을 강제)
    save_term = models.IntegerField(choices=SaveTerm.choices, null=True, blank=True)  # 적금 기간(개월)
    monthly_amount = models.IntegerField(null=True, blank=True)  # 월 저축액(원, 적금), 5만~300만
    deposit_term = models.IntegerField(choices=SaveTerm.choices, null=True, blank=True)  # 예금 예치 기간(개월)
    deposit_amount = models.IntegerField(null=True, blank=True)  # 예치금액(원, 예금), 5만~5000만
    # STEP 02
    birth_date = models.DateField()  # 생년월일 → 만 나이/연령대 매칭에 사용
    # 적금 전용 STEP02 답변. 예금만 쓰는 회원도 있으므로 기본값 False.
    salary_transfer = models.BooleanField(default=False)  # 급여이체 가능 여부
    auto_transfer = models.BooleanField(default=False)  # 자동이체 가능 여부
    card_usage = models.BooleanField(default=False)  # 카드실적 가능 여부
    housing_subscription = models.BooleanField(default=False)  # 주택청약 보유 여부
    # 예금 전용 STEP02 답변. 적금만 쓰던 기존 프로필엔 없던 값이라 기본값 False.
    first_transaction = models.BooleanField(default=False)  # 이 은행 첫거래(신규) 여부
    online_signup = models.BooleanField(default=False)  # 비대면(인터넷·모바일) 가입 의향
    marketing_consent = models.BooleanField(default=False)  # 마케팅·알림 수신 동의 가능
    redeposit = models.BooleanField(default=False)  # 만기 재예치/재가입 의향
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "search_profile"
