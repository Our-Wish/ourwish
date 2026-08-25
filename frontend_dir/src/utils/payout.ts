/**
 * 만기 세후 수령액 계산 — 백엔드 `apps/products/services.py`와 같은 산식.
 *
 * 추천/찜 목록 금액은 서버가 계산해 내려주지만, 상세 계산기는 사용자가
 * 금액·기간·금리를 즉시 바꿔보는 화면이라 프론트에서 직접 계산한다.
 * 두 값이 어긋나지 않도록 산식을 이 파일 한 곳에만 둔다.
 *
 * 단위는 백엔드와 동일하게 '원'. 화면은 만원 단위로 표시하므로
 * 호출부에서 toManwon()을 거친다.
 */

// 이자소득세율 15.4% = 소득세 14% + 지방소득세 1.4%. 원금이 아니라 '이자'에만 부과한다.
export const TAX_RATE = 0.154

/** 'S' 단리 / 'M' 복리(월복리) */
export type IntrRateType = 'S' | 'M'

export type PayoutResult = {
  principal: number // 원금(원) — 적금은 월납입액 × 개월수, 예금은 예치금
  afterTaxInterest: number // 세후이자(원)
  total: number // 원금 + 세후이자(원)
}

/** 세전이자에 과세하고 원 미만을 절사한다. 백엔드의 int(원금 + 세후이자)와 결과가 같다. */
function toResult(principal: number, preTaxInterest: number): PayoutResult {
  const afterTaxInterest = Math.floor(preTaxInterest * (1 - TAX_RATE))
  return { principal, afterTaxInterest, total: principal + afterTaxInterest }
}

/**
 * 적금(적립식) 세후 수령액.
 * 납입 회차마다 이자 기간이 달라, 첫 달 납입금은 n개월치 / 마지막 달은 1개월치 이자만 받는다.
 */
export function calculateSavingsPayout(
  monthlyAmount: number,
  termMonths: number,
  annualRate: number,
  intrRateType: IntrRateType,
): PayoutResult {
  const principal = monthlyAmount * termMonths
  const rate = annualRate / 100 // %(3.5) -> 소수(0.035)

  if (rate === 0) return toResult(principal, 0) // 0% 방어: 이자 0 + 0 나눗셈 방지

  if (intrRateType === 'S') {
    const monthsSum = (termMonths * (termMonths + 1)) / 2 // 1+2+...+n (개월)
    return toResult(principal, monthlyAmount * (rate / 12) * monthsSum)
  }

  // 복리(M) — 월복리. 적립식 연금의 미래가치(FV of annuity).
  const monthlyRate = rate / 12
  const balance = (monthlyAmount * ((1 + monthlyRate) ** termMonths - 1)) / monthlyRate
  return toResult(principal, balance - principal)
}

/**
 * 예금(거치식) 세후 수령액.
 * 목돈을 한 번에 넣고 만기까지 두므로 원금 전액이 전 기간 이자를 받는다.
 */
export function calculateDepositPayout(
  principal: number,
  termMonths: number,
  annualRate: number,
  intrRateType: IntrRateType,
): PayoutResult {
  const rate = annualRate / 100

  if (rate === 0) return toResult(principal, 0)

  if (intrRateType === 'S') {
    return toResult(principal, principal * rate * (termMonths / 12))
  }

  // 복리(M) — 월복리
  const monthlyRate = rate / 12
  return toResult(principal, principal * (1 + monthlyRate) ** termMonths - principal)
}

/** 상품군에 맞는 산식으로 보내주는 얇은 래퍼 (적금=적립식, 예금=거치식). */
export function calculatePayout(params: {
  amount: number // 원 — 적금은 월납입액, 예금은 예치금
  termMonths: number
  annualRate: number // 연이율(%)
  intrRateType: IntrRateType
  isDeposit: boolean
}): PayoutResult {
  const { amount, termMonths, annualRate, intrRateType, isDeposit } = params
  return isDeposit
    ? calculateDepositPayout(amount, termMonths, annualRate, intrRateType)
    : calculateSavingsPayout(amount, termMonths, annualRate, intrRateType)
}

/** 원 -> 만원. 화면 표시 단위가 만원이라 formatWon()에 넣기 전에 거친다. */
export function toManwon(won: number): number {
  return Math.round(won / 10000)
}

/** 만원 -> 원. 입력 폼이 만원 단위라 계산 전에 거친다. */
export function toWon(manwon: number): number {
  return manwon * 10000
}
