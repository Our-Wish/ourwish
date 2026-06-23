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
  }),
  actions: {
    async fetchFavorites() {
      if (this.isFetched) return
      const { data } = await api.get('/api/v1/favorites/')
      console.log('favorites:', data)
      this.favorites = data
      this.isFetched = true
    },
    // 서버에서 먼저 지운 뒤(성공해야) 로컬 목록에서도 제거한다.
    // (로컬만 지우면 서버 DB엔 남아 새로고침/재로그인 시 되살아난다)
    async removeFavorite(productId: number) {
      await api.delete(`/api/v1/favorites/${productId}/`)
      this.favorites = this.favorites.filter((f) => f.product_id !== productId)
    },
  },
})
