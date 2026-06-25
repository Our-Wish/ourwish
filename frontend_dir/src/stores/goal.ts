import { defineStore } from 'pinia'

export const useGoalStore = defineStore('goal', {
  state: () => ({
    savings: {
      period: 12,
      monthlyAmount: 50,
      targetAmount: 0,
    },
    deposit: {
      period: 12,
      amount: 50,
    },
  }),
  actions: {
    setSavingsGoal(period: number, monthlyAmount: number) {
      this.savings.period = period
      this.savings.monthlyAmount = monthlyAmount
    },
    setSavingsTargetAmount(amount: number) {
      this.savings.targetAmount = amount
    },
    setDepositGoal(period: number, amount: number) {
      this.deposit.period = period
      this.deposit.amount = amount
    },
  },
})
