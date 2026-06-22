from django.db import models


# Create your models here.
class Bank(models.Model):
    class BankType(models.TextChoices):
        FIRST_TIER = "FIRST_TIER", "시중은행"
        SAVINGS = "SAVINGS", "저축은행"

    bank_code = models.CharField(max_length=20, primary_key=True)
    bank_name = models.CharField(max_length=100)
    bank_type = models.CharField(max_length=20, choices=BankType.choices)

    class Meta:
        db_table = "bank"


class Product(models.Model):
    class ProductType(models.TextChoices):
        SAVINGS = "SAVINGS", "적금"
        DEPOSIT = "DEPOSIT", "예금"

    bank = models.ForeignKey(Bank, on_delete=models.RESTRICT, related_name="products")
    # 적금(적립식)/예금(거치식) 구분. 기존 데이터는 전부 적금이라 기본값 SAVINGS.
    product_type = models.CharField(
        max_length=20, choices=ProductType.choices, default=ProductType.SAVINGS
    )
    fin_prdt_cd = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    # FSS 원문 필드 — 상품 상세에 그대로 노출.
    join_member = models.CharField(max_length=500, blank=True)
    join_way = models.CharField(max_length=200, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)  # 월 납입 한도 필터에 사용
    # 최소 가입금액(원). FSS 원문엔 구조화 안 돼 있어 LLM이 etc_note 등에서 추출.
    # NULL = 최소금액 정보 없음(하한 필터에서 안 거름).
    min_limit = models.BigIntegerField(null=True, blank=True)
    maturity_interest = models.TextField(blank=True)
    etc_note = models.TextField(blank=True)
    special_condition_raw = models.TextField(blank=True)  # 우대조건 전문(파싱 없이 노출)
    # 매칭 태그 — 이 상품이 해당 우대조건을 제공하는가(LLM 배치 분류).
    tag_salary_transfer = models.BooleanField(default=False)  # 급여이체
    tag_auto_transfer = models.BooleanField(default=False)  # 자동이체
    tag_card_usage = models.BooleanField(default=False)  # 카드실적
    tag_housing_subscription = models.BooleanField(default=False)  # 청약(적금)
    # 예금 전용 태그 — 예금 우대조건 데이터 빈도 상위 4종(적금엔 안 쓰임).
    tag_first_transaction = models.BooleanField(default=False)  # 첫거래/신규
    tag_online_signup = models.BooleanField(default=False)  # 비대면(인터넷·모바일) 가입
    tag_marketing_consent = models.BooleanField(default=False)  # 마케팅·알림 동의
    tag_redeposit = models.BooleanField(default=False)  # 재예치/재가입
    # 가입 연령 제한(NULL=제한 없음). 나이 필터에 사용.
    age_min = models.IntegerField(null=True, blank=True)
    age_max = models.IntegerField(null=True, blank=True)
    # AI 한줄 요약("이런 분께 좋아요") — LLM 배치 생성.
    ai_summary = models.TextField(null=True, blank=True)
    dcls_strt_day = models.CharField(max_length=8, blank=True)
    dcls_end_day = models.CharField(max_length=8, null=True, blank=True)
    synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "product"
        unique_together = [("bank", "fin_prdt_cd")]


class ProductOption(models.Model):
    class IntrRateType(models.TextChoices):
        SIMPLE = "S", "단리"
        COMPOUND = "M", "복리"

    class RsrvType(models.TextChoices):
        FIXED = "S", "정액"
        FREE = "F", "자유"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="options"
    )
    save_term = models.IntegerField()
    intr_rate_type = models.CharField(max_length=1, choices=IntrRateType.choices)
    # 예금(거치식)은 FSS 데이터에 적립유형 자체가 없어 NULL로 둔다(적금만 값이 있음).
    rsrv_type = models.CharField(
        max_length=1, choices=RsrvType.choices, null=True, blank=True
    )
    base_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "product_option"
        unique_together = [("product", "save_term", "intr_rate_type", "rsrv_type")]
