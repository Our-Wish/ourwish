from django.test import SimpleTestCase

from apps.products.models import ProductOption
from apps.products.services import calculate_after_tax_payout


class AfterTaxPayoutTest(SimpleTestCase):
    """만기 세후 수령액 계산 단위 테스트 (DB 불필요 → SimpleTestCase)."""

    MONTHLY = 100_000  # 월 납입액
    TERM = 12          # 납입 개월 수

    def test_simple_interest(self):
        # 단리 3.0%: 원금 120만 + 세후이자 → 1,216,497원
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 3.0, ProductOption.IntrRateType.SIMPLE
        )
        self.assertEqual(result, 1_216_497)

    def test_compound_interest(self):
        # 복리(월복리) 3.0% → 1,214,075원
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 3.0, ProductOption.IntrRateType.COMPOUND
        )
        self.assertEqual(result, 1_214_075)

    def test_zero_rate_returns_principal(self):
        # 이율 0% → 이자 없이 원금(120만)만 (0 나눗셈 방어 동작 확인)
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 0, ProductOption.IntrRateType.SIMPLE
        )
        self.assertEqual(result, 1_200_000)
