"""예·적금 도메인 계산 로직 (세후 수령액, 대표 옵션 선정).

뷰(View)에서 직접 계산하지 않고 이 모듈로 분리해 두면,
추천 API(#7)와 찜 목록 API가 같은 산식을 재사용할 수 있다.
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


def calculate_deposit_after_tax_payout(principal, term_months, annual_rate, intr_rate_type):
    """거치식(예금) 만기 세후 수령액(원금 + 세후이자)을 '원' 단위 정수로 돌려준다.

    적금(적립식)과 달리 목돈을 가입 시점에 한 번에 넣고 만기까지 그대로 둔다.
    principal:      예치금(원, int)
    term_months:    예치 기간(개월, int)
    annual_rate:    연이율(%) — 예: 3.50
    intr_rate_type: 'S'(단리) 또는 'M'(복리, 월복리로 계산)
    """
    rate = Decimal(str(annual_rate)) / Decimal(100)        # %(3.50) -> 소수(0.035)

    if rate == 0:                                           # 0% 방어: 이자 0
        return principal

    if intr_rate_type == ProductOption.IntrRateType.SIMPLE:    # 단리(S)
        pre_tax_interest = principal * rate * Decimal(term_months) / Decimal(12)
    else:                                                       # 복리(M) — 월복리
        monthly_rate = rate / 12
        balance = principal * ((1 + monthly_rate) ** term_months)
        pre_tax_interest = balance - principal

    after_tax_interest = pre_tax_interest * (1 - TAX_RATE)     # 이자에만 과세
    return int(principal + after_tax_interest)                # 원 미만 절사


def calculate_payout(amount, term_months, annual_rate, intr_rate_type, is_deposit):
    """상품군에 맞는 산식으로 세후 수령액 계산 (적금=적립식, 예금=거치식)."""
    if is_deposit:
        return calculate_deposit_after_tax_payout(
            amount, term_months, annual_rate, intr_rate_type
        )
    return calculate_after_tax_payout(amount, term_months, annual_rate, intr_rate_type)


def best_option_by_payout(options, amount, use_max, is_deposit):
    """옵션 중 세후 수령액이 가장 큰 것을 (option, payout)으로 반환. 옵션이 없으면 None.

    use_max=True면 최고금리(없으면 기본금리로 폴백), False면 기본금리로 계산한다.
    추천 목록(#7)과 찜 목록이 '대표 옵션'을 같은 기준으로 고르도록 공용화했다.
    """
    best = None
    for option in options:
        rate = (
            option.max_rate
            if use_max and option.max_rate is not None
            else option.base_rate
        )
        payout = calculate_payout(
            amount, option.save_term, rate, option.intr_rate_type, is_deposit
        )
        if best is None or payout > best[1]:
            best = (option, payout)
    return best
