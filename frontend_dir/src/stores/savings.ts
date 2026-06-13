import { defineStore } from 'pinia'

export type MySavingsProduct = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  dDay: number
  currentAmount: number
  maturityAmount: number
  progress: number
  nextPaymentDate: string
  monthlyAmount: number
}

export const useSavingsStore = defineStore('savings', {
  state: () => ({
    myProducts: [] as MySavingsProduct[],
  }),
  actions: {
    addProduct(product: MySavingsProduct) {
      if (!this.myProducts.find((p) => p.id === product.id)) {
        this.myProducts.push(product)
      }
    },
  },
})
