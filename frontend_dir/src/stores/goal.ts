import { defineStore } from 'pinia'

export const useGoalStore = defineStore('goal', {
  state: () => ({
    period: 12,
    monthlyAmount: 50,
    targetAmount: 0,
  }),
  actions: {
    setGoal(period: number, monthlyAmount: number) {
      this.period = period
      this.monthlyAmount = monthlyAmount
    },
    setTargetAmount(amount: number) {
      this.targetAmount = amount
    },
  },
})
