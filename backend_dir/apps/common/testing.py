"""API 테스트 공통 재료 — 회원·은행·상품 픽스처를 한 줄로 만든다.

각 앱 tests.py가 같은 셋업을 반복하지 않도록 모아둔다(테스트 전용, 운영 코드에서 import 금지).
"""
from datetime import date

from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient

from apps.accounts.models import Member, SearchProfile
from apps.products.models import Bank, Product, ProductOption


def make_member(login_id="tester", password="pass1234", nickname="테스터"):
    return Member.objects.create(
        login_id=login_id, password_hash=make_password(password), nickname=nickname
    )


def make_profile(member, **overrides):
    """적금(12개월·30만원)+예금(24개월·1000만원) 둘 다 채운 프로필."""
    data = dict(
        save_term=12, monthly_amount=300_000,
        deposit_term=24, deposit_amount=10_000_000,
        birth_date=date(1999, 1, 1),
        salary_transfer=True, auto_transfer=False, card_usage=False, housing_subscription=False,
    )
    data.update(overrides)
    return SearchProfile.objects.create(member=member, **data)


def make_product(name="테스트적금", product_type=Product.ProductType.SAVINGS,
                 terms=(12,), base_rate="3.00", max_rate="4.00", **fields):
    """은행 1개 + 상품 1개 + 기간별 옵션(단리). 같은 은행은 재사용한다."""
    bank, _ = Bank.objects.get_or_create(
        bank_code="0000001", defaults={"bank_name": "테스트은행", "bank_type": Bank.BankType.FIRST_TIER}
    )
    product = Product.objects.create(
        bank=bank, product_type=product_type, fin_prdt_cd=f"P-{name}", product_name=name, **fields
    )
    for term in terms:
        ProductOption.objects.create(
            product=product, save_term=term, intr_rate_type=ProductOption.IntrRateType.SIMPLE,
            rsrv_type=ProductOption.RsrvType.FIXED if product_type == Product.ProductType.SAVINGS else None,
            base_rate=base_rate, max_rate=max_rate,
        )
    return product


def auth_client(member=None):
    """로그인된 APIClient. member=None이면 비로그인 클라이언트."""
    client = APIClient()
    if member is not None:
        client.force_authenticate(user=member)
    return client
