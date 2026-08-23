import { defineStore } from 'pinia'

// 새로고침해도 플랜(기간·금액)이 유지되도록 sessionStorage에 저장한다.
// (탭을 닫으면 사라짐 — 로그인 토큰과 같은 수명)
const STORAGE_KEY = 'goal'

// STEP2 우대조건 답변 — 비로그인 사용자는 서버 프로필 대신 여기에 둔다.
export type SavingsAnswers = {
  salary_transfer: boolean
  auto_transfer: boolean
  card_usage: boolean
  housing_subscription: boolean
}
export type DepositAnswers = {
  first_transaction: boolean
  online_signup: boolean
  marketing_consent: boolean
  redeposit: boolean
}

type GoalState = {
  savings: { period: number; monthlyAmount: number; answers: SavingsAnswers | null }
  deposit: { period: number; amount: number; answers: DepositAnswers | null }
  birthDate: string // 'YYYY-MM-DD', 미입력이면 ''
}

const defaultState = (): GoalState => ({
  savings: { period: 12, monthlyAmount: 50, answers: null },
  deposit: { period: 12, amount: 50, answers: null },
  birthDate: '',
})

// 저장된 값이 있으면 그걸로, 없거나 깨져 있으면 기본값으로 시작한다.
function loadState(): GoalState {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (!raw) return defaultState()
    const saved = JSON.parse(raw) as Partial<GoalState>
    return { ...defaultState(), ...saved }
  } catch {
    return defaultState()
  }
}

export const useGoalStore = defineStore('goal', {
  state: (): GoalState => loadState(),
  actions: {
    persist() {
      sessionStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ savings: this.savings, deposit: this.deposit, birthDate: this.birthDate }),
      )
    },
    setSavingsGoal(period: number, monthlyAmount: number, answers?: SavingsAnswers) {
      this.savings.period = period
      this.savings.monthlyAmount = monthlyAmount
      if (answers) this.savings.answers = answers
      this.persist()
    },
    setDepositGoal(period: number, amount: number, answers?: DepositAnswers) {
      this.deposit.period = period
      this.deposit.amount = amount
      if (answers) this.deposit.answers = answers
      this.persist()
    },
    setBirthDate(birthDate: string) {
      this.birthDate = birthDate
      this.persist()
    },
    // 서버에 저장된 조회 프로필(원 단위)로 플랜을 맞춘다 — 새 탭/기기에서도 숫자가 맞도록.
    syncFromProfile(profile: {
      save_term?: number
      monthly_amount?: number | null
      deposit_amount?: number | null
    }) {
      if (profile.save_term) {
        this.savings.period = profile.save_term
        this.deposit.period = profile.save_term
      }
      if (profile.monthly_amount) this.savings.monthlyAmount = profile.monthly_amount / 10000
      if (profile.deposit_amount) this.deposit.amount = profile.deposit_amount / 10000
      this.persist()
    },
    // 로그아웃용 — 저장본까지 지우고 기본값으로 되돌린다.
    clear() {
      sessionStorage.removeItem(STORAGE_KEY)
      Object.assign(this, defaultState())
    },
  },
})
