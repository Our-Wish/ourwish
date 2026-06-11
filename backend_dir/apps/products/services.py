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
