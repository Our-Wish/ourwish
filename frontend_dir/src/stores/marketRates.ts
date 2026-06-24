import { defineStore } from 'pinia'
import api from '@/api/index'

// 한국은행 예금은행 수신금리(연 %) — STEP1 예상 수령액의 '평균 금리' 기준값.
// 초기값은 폴백(기존 박제값)으로 둬, 조회 전/실패 시에도 계산이 동작하게 한다.
export const useMarketRatesStore = defineStore('marketRates', {
  state: () => ({
    depositAvg: 3.5, // 정기예금 평균(연 %)
    savingsAvg: 4.0, // 정기적금 평균(연 %)
    asOf: '' as string | null, // 기준 월 'YYYY-MM'
    loaded: false,
  }),
  actions: {
    async fetchMarketRates() {
      // 금리는 월 단위로만 바뀌므로 세션당 한 번만 받아온다.
      if (this.loaded) return
      try {
        const { data } = await api.get('/api/v1/products/market-rates/')
        this.depositAvg = data.deposit_avg
        this.savingsAvg = data.savings_avg
        this.asOf = data.as_of
        this.loaded = true
      } catch {
        // 실패해도 초기 폴백값(3.5/4.0)을 유지해 STEP1 계산이 깨지지 않게 한다.
      }
    },
  },
})
