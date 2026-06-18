"""적금 도메인 계산 로직 (세후 수령액 등).

뷰(View)에서 직접 계산하지 않고 이 모듈로 분리해 두면,
추천 API(#7)와 가입 API(#9)가 같은 산식을 재사용할 수 있다.
"""
from decimal import Decimal

from apps.products.models import ProductOption

# 이자소득세율 15.4% = 소득세 14% + 지방소득세 1.4%. 원금이 아니라 '이자'에만 부과한다.
TAX_RATE = Decimal("0.154")


def calculate_after_tax_payout(monthly_amount, term_months, annual_rate, intr_rate_type):
    """정액적금 만기 세후 수령액(원금 + 세후이자)을 '원' 단위 정수로 돌려준다.

    monthly_amount: 매월 납입액(원, int)
    term_months:    납입 개월 수(int)
    annual_rate:    연이율(%) — 예: 3.50
    intr_rate_type: 'S'(단리) 또는 'M'(복리)
    """
    principal = monthly_amount * term_months              # 총 납입 원금
    rate = Decimal(str(annual_rate)) / Decimal(100)       # %(3.50) -> 소수(0.035)

    if rate == 0:                                         # 0% 방어: 이자 0 + 0 나눗셈 방지
        return principal

    if intr_rate_type == ProductOption.IntrRateType.SIMPLE:    # 단리(S)
        months_sum = term_months * (term_months + 1) // 2      # 1+2+...+n (개월)
        pre_tax_interest = monthly_amount * (rate / 12) * months_sum
    else:                                                      # 복리(M) — 월복리
        monthly_rate = rate / 12
        balance = monthly_amount * (((1 + monthly_rate) ** term_months) - 1) / monthly_rate
        pre_tax_interest = balance - principal

    after_tax_interest = pre_tax_interest * (1 - TAX_RATE)     # 이자에만 과세
    return int(principal + after_tax_interest)                # 원 미만 절사


def calculate_applied_rate(base_rate, max_rate, condition_rates):
    """적용금리(%) = 기본금리 + 체크한 우대조건 rate들의 합. max_rate가 있으면 그 이하로 cap.

    base_rate:       ProductOption.base_rate (Decimal, %)
    max_rate:        ProductOption.max_rate (Decimal 또는 None, %)
    condition_rates: 사용자가 체크한 PreferentialCondition.rate들의 리스트(Decimal)
    """
    applied = base_rate + sum(condition_rates, Decimal("0"))   # 기본금리 + 우대 가산분
    if max_rate is not None:                                   # 최고금리 상한이 있으면
        applied = min(applied, max_rate)                       # 그 위로는 못 올라간다
    return applied


# 조건 difficulty → 순위(클수록 어렵다). None이면 가장 어려운 HIGH(3)로 취급.
DIFFICULTY_RANK = {"LOW": 1, "MID": 2, "HIGH": 3}
# 응답 난이도 키 → 포함 임계. BASE(0) = 우대조건을 하나도 안 챙긴 '기본금리'.
_LEVEL_THRESHOLDS = {"BASE": 0, "LOW": 1, "MID": 2, "HIGH": 3}


def calculate_rate_by_difficulty(option, conditions, summary_labels, monthly_amount=None):
    """옵션 1개 기준, 난이도별(BASE/LOW/MID/HIGH) 누적 우대금리·예상금리를 계산한다.

    BASE = 우대조건을 하나도 적용하지 않은 기본금리. LOW/MID/HIGH는 누적이라,
    난이도 d를 고른 사용자는 'd 이하' 조건을 모두 달성한다고 본다(MID = LOW+MID 전부).
    difficulty가 None인 조건은 HIGH로 취급. max_rate가 있으면 그 이하로 상한(cap).
    monthly_amount가 주어지면 expected_payout(세후수령액)까지 계산한다(목록 #7용).
    상세 #8은 납입액이 없어 payout 없이 호출한다.

    option:         ProductOption (base_rate·max_rate·save_term·intr_rate_type 사용)
    conditions:     이 상품의 PreferentialCondition 목록
    summary_labels: {"LOW": ..., "MID": ..., "HIGH": ...} 난이도별 요약 문구 (BASE는 None)
    """
    result = {}
    for level, threshold in _LEVEL_THRESHOLDS.items():
        included = [
            c for c in conditions if DIFFICULTY_RANK.get(c.difficulty, 3) <= threshold
        ]
        bonus = sum((c.rate for c in included), Decimal("0"))
        expected = option.base_rate + bonus
        if option.max_rate is not None:
            expected = min(expected, option.max_rate)

        entry = {
            "bonus_rate": float(bonus),
            "expected_rate": float(expected),
            "condition_ids": [c.id for c in included],
            "summary_label": summary_labels.get(level),
        }
        if monthly_amount is not None:
            entry["expected_payout"] = calculate_after_tax_payout(
                monthly_amount, option.save_term, expected, option.intr_rate_type
            )
        result[level] = entry
    return result
