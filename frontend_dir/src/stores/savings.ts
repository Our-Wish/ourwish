import { defineStore } from 'pinia'
import api from '@/api/index'

export interface Enrollment {
  enrollment_id: number
  product_id: number
  product_name: string
  bank_name: string
  product_type: 'DEPOSIT' | 'SAVINGS'
  is_filled: boolean
  monthly_amount: number
  deposit_amount: number
  rate: number
  start_date: string
  maturity_date: string
  achievement_gauge: number
}

export const useSavingsStore = defineStore('savings', {
  state: () => ({
    enrollments: [] as Enrollment[],
    isFetched: false,
  }),
  actions: {
    async fetchEnrollments() {
      if (this.isFetched) return
      const { data } = await api.get('/api/v1/enrollments/')
      this.enrollments = data
      this.isFetched = true
    },
    addEnrollment(enrollment: Enrollment) {
      this.enrollments.push(enrollment)
    },
    updateEnrollment(updated: Enrollment) {
      const idx = this.enrollments.findIndex((e) => e.enrollment_id === updated.enrollment_id)
      if (idx !== -1) this.enrollments[idx] = updated
    },
    removeEnrollment(enrollmentId: number) {
      this.enrollments = this.enrollments.filter((e) => e.enrollment_id !== enrollmentId)
    },
  },
})
