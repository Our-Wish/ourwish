import { defineStore } from 'pinia'
import api from '@/api/index'

export interface Favorite {
  product_id: number
  bank_name: string
  bank_type: string
  product_name: string
  product_type: 'DEPOSIT' | 'SAVINGS'
  base_rate: number
  max_rate: number
  expected_payout: number
}

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    favorites: [] as Favorite[],
    isFetched: false,
    isLoading: false,
  }),
  actions: {
    async fetchFavorites() {
      if (this.isFetched) return
      this.isLoading = true
      try {
        const { data } = await api.get('/api/v1/favorites/')
        this.favorites = data
        this.isFetched = true
      } finally {
        this.isLoading = false
      }
    },
    // 찜 추가. 목록 한 줄에 들어갈 금리·예상 수령액은 서버만 계산할 수 있으므로
    // 여기서 직접 push하지 않고, 다음에 목록을 열 때 다시 받아오게 표시만 해둔다.
    async addFavorite(productId: number) {
      await api.post('/api/v1/favorites/', { product_id: productId })
      this.isFetched = false
    },
    // 서버에서 먼저 지운 뒤(성공해야) 로컬 목록에서도 제거한다.
    async removeFavorite(productId: number) {
      await api.delete(`/api/v1/favorites/${productId}/`)
      this.favorites = this.favorites.filter((f) => f.product_id !== productId)
    },
  },
})
