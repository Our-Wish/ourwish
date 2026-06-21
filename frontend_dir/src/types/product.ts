export type Condition = { label: string; value: string }

export type ProductDetail = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  baseRate: number
  maxRate: number
  intr_rate_type: string
  rsrv_type: string
  conditions: Condition[]
  specialCondition: string
  aiSummaries: string[]
  tags: string[]
}
