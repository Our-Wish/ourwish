from decimal import Decimal

from django.test import SimpleTestCase

from apps.products.models import PreferentialCondition, ProductOption
from apps.products.services import (
    calculate_after_tax_payout,
    calculate_applied_rate,
    calculate_rate_by_difficulty,
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


def _cond(cond_id, difficulty, rate):
    # 저장하지 않은 메모리상 인스턴스 (계산 함수는 DB를 안 봐서 충분).
    return PreferentialCondition(
        id=cond_id, difficulty=difficulty, rate=Decimal(str(rate))
    )


def _option(base_rate, max_rate=None, term=12):
    return ProductOption(
        save_term=term,
        intr_rate_type=ProductOption.IntrRateType.SIMPLE,
        base_rate=Decimal(str(base_rate)),
        max_rate=Decimal(str(max_rate)) if max_rate is not None else None,
    )


class RateByDifficultyTest(SimpleTestCase):
    """난이도별 누적 금리 계산 단위 테스트 (DB 불필요 → SimpleTestCase)."""

    def test_cumulative_bonus(self):
        # BASE=우대 0개, LOW=LOW들, MID=LOW+MID, HIGH=전부. 상한 없음.
        conds = [
            _cond(1, "LOW", 0.8), _cond(2, "LOW", 0.2),
            _cond(3, "MID", 1.0), _cond(4, "HIGH", 1.0),
        ]
        r = calculate_rate_by_difficulty(_option(3.0), conds, {})
        self.assertEqual(r["BASE"]["expected_rate"], 3.0)   # 우대 0개 = 기본금리
        self.assertEqual(r["BASE"]["bonus_rate"], 0.0)
        self.assertEqual(r["BASE"]["condition_ids"], [])
        self.assertEqual(r["LOW"]["expected_rate"], 4.0)    # 3 + (0.8+0.2)
        self.assertEqual(r["MID"]["expected_rate"], 5.0)    # 3 + (0.8+0.2+1.0)
        self.assertEqual(r["HIGH"]["expected_rate"], 6.0)   # 3 + 3.0
        self.assertEqual(r["LOW"]["condition_ids"], [1, 2])
        self.assertEqual(r["HIGH"]["condition_ids"], [1, 2, 3, 4])

    def test_max_rate_cap(self):
        # max_rate가 있으면 그 이하로 잘린다.
        conds = [_cond(1, "LOW", 0.8), _cond(2, "MID", 1.0), _cond(3, "HIGH", 1.0)]
        r = calculate_rate_by_difficulty(_option(3.0, max_rate=4.5), conds, {})
        self.assertEqual(r["LOW"]["expected_rate"], 3.8)    # 상한 미만
        self.assertEqual(r["MID"]["expected_rate"], 4.5)    # 3+1.8=4.8 → 4.5로 cap
        self.assertEqual(r["HIGH"]["expected_rate"], 4.5)   # 3+2.8=5.8 → 4.5로 cap

    def test_null_difficulty_treated_as_high(self):
        # difficulty가 None인 조건은 HIGH로 취급(LOW/MID엔 안 들어감).
        conds = [_cond(1, "LOW", 0.5), _cond(2, None, 1.0)]
        r = calculate_rate_by_difficulty(_option(3.0), conds, {})
        self.assertEqual(r["LOW"]["expected_rate"], 3.5)    # None 제외
        self.assertEqual(r["MID"]["expected_rate"], 3.5)    # None 제외
        self.assertEqual(r["HIGH"]["expected_rate"], 4.5)   # None 포함
        self.assertEqual(r["HIGH"]["condition_ids"], [1, 2])

    def test_summary_label_passthrough(self):
        r = calculate_rate_by_difficulty(
            _option(3.0), [_cond(1, "LOW", 0.5)],
            {"LOW": "쉬운 요약", "MID": None, "HIGH": None},
        )
        self.assertEqual(r["LOW"]["summary_label"], "쉬운 요약")
        self.assertIsNone(r["MID"]["summary_label"])

    def test_expected_payout_only_when_monthly_given(self):
        # monthly_amount를 주면 payout 계산(우대 없으면 단리 3% 기준값), 안 주면 키 없음.
        with_payout = calculate_rate_by_difficulty(
            _option(3.0), [], {}, monthly_amount=100_000
        )
        self.assertEqual(with_payout["LOW"]["expected_payout"], 1_216_497)

        without_payout = calculate_rate_by_difficulty(_option(3.0), [], {})
        self.assertNotIn("expected_payout", without_payout["LOW"])
