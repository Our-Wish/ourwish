import { defineStore } from 'pinia'

// 새로고침해도 플랜(기간·금액)이 유지되도록 sessionStorage에 저장한다.
// (탭을 닫으면 사라짐 — 로그인 토큰과 같은 수명)
const STORAGE_KEY = 'goal'

type GoalState = {
  savings: { period: number; monthlyAmount: number }
  deposit: { period: number; amount: number }
}

const defaultState = (): GoalState => ({
  savings: { period: 12, monthlyAmount: 50 },
  deposit: { period: 12, amount: 50 },
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
        JSON.stringify({ savings: this.savings, deposit: this.deposit }),
      )
    },
    setSavingsGoal(period: number, monthlyAmount: number) {
      this.savings.period = period
      this.savings.monthlyAmount = monthlyAmount
      this.persist()
    },
    setDepositGoal(period: number, amount: number) {
      this.deposit.period = period
      this.deposit.amount = amount
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
