from decimal import Decimal

from django.test import SimpleTestCase

from apps.products.models import ProductOption
from apps.products.services import (
    calculate_after_tax_payout,
    calculate_applied_rate,
)


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


class AppliedRateTest(SimpleTestCase):
    """적용금리(기본 + 우대 합산, max_rate 상한) 계산 단위 테스트."""

    def test_sum_without_cap(self):
        # 상한 없음: 기본 2.0 + 우대(0.3 + 0.2) = 2.5
        result = calculate_applied_rate(
            Decimal("2.0"), None, [Decimal("0.3"), Decimal("0.2")]
        )
        self.assertEqual(result, Decimal("2.5"))

    def test_capped_by_max_rate(self):
        # 합이 2.5라도 max_rate 2.4가 상한이면 2.4로 cap
        result = calculate_applied_rate(
            Decimal("2.0"), Decimal("2.4"), [Decimal("0.3"), Decimal("0.2")]
        )
        self.assertEqual(result, Decimal("2.4"))

    def test_no_conditions(self):
        # 체크한 우대조건이 없으면 기본금리 그대로
        result = calculate_applied_rate(Decimal("2.0"), Decimal("3.0"), [])
        self.assertEqual(result, Decimal("2.0"))
