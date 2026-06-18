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
    bank = models.ForeignKey(Bank, on_delete=models.RESTRICT, related_name="products")
    fin_prdt_cd = models.CharField(max_length=50)
    product_name = models.CharField(max_length=200)
    join_member = models.CharField(max_length=500, blank=True)
    join_way = models.CharField(max_length=200, blank=True)
    max_limit = models.BigIntegerField(null=True, blank=True)
    maturity_interest = models.TextField(blank=True)
    etc_note = models.TextField(blank=True)
    special_condition_raw = models.TextField(blank=True)
    has_bonus = models.BooleanField(default=False)
    maturity_summary = models.TextField(null=True, blank=True)
    join_summary = models.TextField(null=True, blank=True)
    etc_summary = models.TextField(null=True, blank=True)
    # 난이도별(LOW/MID/HIGH) 요약 문구 — rate_by_difficulty의 summary_label용 (LLM 생성).
    summary_label_low = models.TextField(null=True, blank=True)
    summary_label_mid = models.TextField(null=True, blank=True)
    summary_label_high = models.TextField(null=True, blank=True)
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
    rsrv_type = models.CharField(max_length=1, choices=RsrvType.choices)
    base_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )

    class Meta:
        db_table = "product_option"
        unique_together = [("product", "save_term", "intr_rate_type", "rsrv_type")]


class PreferentialCondition(models.Model):
    class Difficulty(models.TextChoices):
        LOW = "LOW", "쉬움"
        MID = "MID", "보통"
        HIGH = "HIGH", "어려움"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="conditions"
    )
    label = models.CharField(max_length=500)
    friendly_label = models.CharField(max_length=500, null=True, blank=True)
    difficulty = models.CharField(
        max_length=4, choices=Difficulty.choices, null=True, blank=True
    )
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        db_table = "preferential_condition"
        unique_together = [("product", "label")]
