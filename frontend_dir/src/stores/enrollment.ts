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
  rate: number | null
  base_rate: number | null // 상품 대표(최고금리) 옵션의 기본금리
  max_rate: number | null
  start_date: string | null
  maturity_date: string | null
  achievement_gauge: number | null // 정보 입력 전엔 null
}

export const useEnrollmentStore = defineStore('enrollment', {
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
    // 서버에서 먼저 지운 뒤(성공해야) 로컬 목록에서도 제거한다.
    async removeEnrollment(enrollmentId: number) {
      await api.delete(`/api/v1/enrollments/${enrollmentId}/`)
      this.enrollments = this.enrollments.filter((e) => e.enrollment_id !== enrollmentId)
    },
  },
})
