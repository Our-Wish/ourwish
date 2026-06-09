import { defineStore } from 'pinia'

export const useGoalStore = defineStore('goal', {
  state: () => ({
    period: 12,
    monthlyAmount: 50,
  }),
  actions: {
    setGoal(period: number, monthlyAmount: number) {
      this.period = period
      this.monthlyAmount = monthlyAmount
    },
  },
})
