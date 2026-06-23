export type Condition = { label: string; value: string }

export type EnrolledProductCardProps = {
  id: number
  productId: number
  bankName: string
  bankColor: string
  productName: string
  productType: string
  isFilled: boolean
  progress: number
  monthlyAmount: number
  rate: number
  startDate: string
  maturityDate: string
}

export type ProductDetail = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  baseRate: number
  maxRate: number
  intr_rate_type: string
  rsrv_type: string
  productType: 'deposit' | 'savings'
  conditions: Condition[]
  specialCondition: string
  aiSummaries: string[]
  tags: string[]
}
