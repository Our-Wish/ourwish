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
    removeFavorite(productId: number) {
      this.favorites = this.favorites.filter((f) => f.product_id !== productId)
    },
  },
})
