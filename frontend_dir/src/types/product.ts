export type Condition = { label: string; value: string }

export type EnrolledProductCardProps = {
  id: number
  productId: number
  bankName: string
  bankColor: string
  productName: string
  productType: 'DEPOSIT' | 'SAVINGS'
  isFilled: boolean
  progress: number
  monthlyAmount: number
  depositAmount: number
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

// ── 백엔드 원본 응답(snake_case) ──
// API가 내려주는 모양 그대로. 화면용 타입(camelCase)으로 바꾸기 전 단계에서 쓴다.

// 추천 목록 한 건 원본 (GET /products/recommend/)
export type RecommendItemApi = {
  product_id: number
  bank_name: string
  bank_type: string
  product_type: 'DEPOSIT' | 'SAVINGS'
  product_name: string
  save_term: number
  base_rate: number
  max_rate: number | null
  expected_payout: number
  matched_tags: string[]
}

// 상세의 옵션 한 개 원본
export type ProductOptionApi = {
  save_term: number
  intr_rate_type: string
  rsrv_type: string | null
  base_rate: number
  max_rate: number | null
}

// 상품 상세 원본 (GET /products/:id/)
export type ProductDetailApi = {
  product_id: number
  bank_name: string
  bank_type: string
  product_type: 'DEPOSIT' | 'SAVINGS'
  product_name: string
  join_member: string
  join_way: string
  max_limit: number | null
  maturity_interest: string
  etc_note: string
  special_condition_raw: string
  ai_summary: string | null
  tags: Record<string, boolean>
  age_min: number | null
  age_max: number | null
  is_favorited: boolean
  base_rate: number | null
  max_rate: number | null
  options: ProductOptionApi[]
}
