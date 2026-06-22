from django.db import models
from django.utils import timezone

from apps.accounts.models import Member
from apps.products.models import Product


class Enrollment(models.Model):
    """내가 등록한 적금/예금. 2단계로 채워진다.

    ① 등록: member·product만 채워진 상태(상세 필드 NULL).
    ② 정보입력: rate·start_date·maturity_date + 금액을 유저가 직접 입력.
       금액은 상품군에 따라 적금=monthly_amount(월납입), 예금=deposit_amount(예치원금).
    달성 게이지는 저장하지 않고 조회할 때 계산한다(시간 기반).
    """

    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="enrollments"
    )
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="enrollments"
    )
    # 정보입력(2단계) 전엔 비어있음 → nullable.
    monthly_amount = models.IntegerField(null=True, blank=True)  # 월 납입액(원, 적금)
    deposit_amount = models.IntegerField(null=True, blank=True)  # 예치 원금(원, 예금)
    rate = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # 실제 계약 금리(%)
    start_date = models.DateField(null=True, blank=True)  # 적금 시작일
    maturity_date = models.DateField(null=True, blank=True)  # 만기일
    created_at = models.DateTimeField(default=timezone.now)  # 우리 앱에 등록한 시각

    class Meta:
        db_table = "enrollment"
        unique_together = [("member", "product")]
