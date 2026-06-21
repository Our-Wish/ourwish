<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div v-if="isLoading" class="flex items-center justify-center py-24 text-slate-400">
      불러오는 중...
    </div>

    <div v-else-if="product" class="mx-auto max-w-6xl px-8 pb-16 pt-6">
      <ProductHeaderCard
        :product="product"
        :is-favorite="isFavorite"
        :bonus-rate="bonusRate"
        :bank-url="bankUrl"
        @toggle-favorite="toggleFavorite"
        @select-product="selectProduct"
      />

      <!-- 본문 2칼럼 -->
      <div class="flex items-start gap-5">
        <!-- 왼쪽 (3/5) -->
        <div class="w-3/5 space-y-4">
          <!-- 한눈에 요약 -->
          <div class="rounded-2xl bg-blue-50 p-6">
            <div class="flex items-center gap-2">
              <svg
                class="h-5 w-5 text-blue-500"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path
                  d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
                />
              </svg>
              <p class="text-base font-bold text-blue-700">한눈에 요약</p>
            </div>
            <ul class="mt-4 space-y-3">
              <li v-for="(s, i) in product.aiSummaries" :key="i" class="flex items-start gap-3">
                <svg
                  class="mt-0.5 h-5 w-5 shrink-0 text-blue-500"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M4.5 12.75l6 6 9-13.5" />
                </svg>
                <span class="text-base text-slate-700">{{ s }}</span>
              </li>
            </ul>
          </div>

          <!-- 상품 기본 정보 -->
          <ProductBasicInfo :conditions="product.conditions" />

          <!-- 우대금리 조건 -->
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <p class="text-base font-semibold text-slate-800">우대 조건 안내</p>
            <div v-if="product.specialCondition" class="mt-4">
              <p class="mt-2 whitespace-pre-line text-sm leading-relaxed text-slate-600">
                {{ product.specialCondition }}
              </p>
            </div>
            <p v-else class="mt-4 text-sm text-slate-400">우대 조건 정보가 없는 상품이에요</p>
          </div>
        </div>

        <!-- 오른쪽 (2/5): 지도 + 챗봇 -->
        <div class="w-2/5 space-y-4">
          <!-- 근처 영업점 -->
          <div class="rounded-2xl bg-white p-5 shadow-sm">
            <p class="text-base font-bold text-slate-900">근처 영업점 찾기</p>
            <div
              class="mt-4 flex h-44 items-center justify-center rounded-xl bg-slate-100 text-sm text-slate-400"
            >
              지도 영역 (카카오맵)
            </div>
            <div class="mt-4 divide-y divide-slate-100">
              <div v-for="i in 2" :key="i" class="flex items-start gap-3 py-3">
                <div
                  class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-500 text-xs font-bold text-white"
                >
                  {{ i }}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <p class="text-sm font-medium text-slate-300">- -</p>
                    <span class="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-400"
                      >영업점</span
                    >
                  </div>
                  <p class="mt-0.5 text-sm text-slate-300">위치 정보 없음</p>
                </div>
              </div>
            </div>
            <button
              class="mt-3 w-full rounded-xl border border-slate-200 py-2 text-sm text-slate-400 transition hover:border-slate-300 hover:text-slate-600"
            >
              더 많은 지점 보기 ∨
            </button>
          </div>

          <!-- 챗봇 -->
          <div class="overflow-hidden rounded-2xl bg-white shadow-sm">
            <div class="flex items-center gap-3 bg-blue-500 px-5 py-4">
              <div
                class="flex h-9 w-9 items-center justify-center rounded-full bg-white/20 text-lg"
              >
                🤖
              </div>
              <div>
                <p class="text-base font-semibold text-white">OURWISH 챗봇</p>
                <div class="flex items-center gap-1.5">
                  <div class="h-2 w-2 rounded-full bg-green-400"></div>
                  <p class="text-sm text-blue-100">온라인</p>
                </div>
              </div>
            </div>
            <Chat :productId="product.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import api from '@/api/index'
import { bankColorMap } from '@/constants/bankColors'
import { BANK_URL_MAP } from '@/constants/bankUrls'
import Chat from '@/components/Chat.vue'
import ProductHeaderCard from '@/components/SavingsDetail/ProductHeaderCard.vue'
import ProductBasicInfo from '@/components/SavingsDetail/ProductBasicInfo.vue'

const router = useRouter()
const route = useRoute()
const goalStore = useGoalStore()

const productId = computed(() => Number(route.params.id))

const isLoading = ref(false)
const isFavorite = ref(false)

type Condition = { label: string; value: string }

const TAG_LABELS: Record<string, string> = {
  salary_transfer: '급여이체',
  auto_transfer: '자동이체',
  card_usage: '카드실적',
  housing_subscription: '주택청약',
}

type ProductDetail = {
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

const product = ref<ProductDetail | null>(null)

function formatLimit(value: number): string {
  if (!value || value > 9e15) return '제한 없음'
  return `${Math.round(value / 10000).toLocaleString()}만원`
}

function buildProduct(data: any): ProductDetail {
  const matchedOption =
    (data.options ?? []).find((o: any) => o.save_term === goalStore.period) ??
    data.options?.[0] ??
    {}

  return {
    id: data.product_id,
    bankName: data.bank_name,
    bankColor: bankColorMap[data.bank_name] ?? '#6366f1',
    productName: data.product_name,
    baseRate: matchedOption.base_rate ?? data.base_rate ?? 0,
    maxRate: matchedOption.max_rate ?? data.max_rate ?? 0,
    intr_rate_type: matchedOption.intr_rate_type ?? 'S',
    rsrv_type: matchedOption.rsrv_type ?? 'S',
    conditions: [
      { label: '가입 대상', value: data.join_member ?? '-' },
      { label: '가입 방법', value: data.join_way ?? '-' },
      { label: '월 납입 한도', value: formatLimit(data.max_limit) },
      { label: '만기후 이자율', value: data.maturity_interest ?? '-' },
      { label: '기타 유의사항', value: data.etc_note ?? '-' },
    ],
    specialCondition: data.special_condition_raw ?? '',
    aiSummaries: data.ai_summary ? data.ai_summary.split('\n').filter(Boolean) : [],
    tags: Object.entries(data.tags ?? {})
      .filter(([, v]) => v)
      .map(([k]) => TAG_LABELS[k] ?? k),
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    const { data } = await api.get(`/api/v1/products/${productId.value}/`)
    product.value = buildProduct(data)
    isFavorite.value = data.is_favorited ?? false
  } catch {
    alert('상품 정보를 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
})

const bankUrl = computed(() =>
  product.value ? (BANK_URL_MAP[product.value.bankName as keyof typeof BANK_URL_MAP] ?? '#') : '#',
)

const bonusRate = computed(() => {
  if (!product.value) return 0
  return Math.max(0, product.value.maxRate - product.value.baseRate)
})

async function toggleFavorite() {
  if (!product.value) return
  try {
    if (isFavorite.value) {
      await api.delete(`/api/v1/favorites/${product.value.id}/`)
    } else {
      await api.post('/api/v1/favorites/', { product_id: product.value.id })
    }
    isFavorite.value = !isFavorite.value
    alert(isFavorite.value ? '관심 상품에 추가했어요.' : '관심 상품에서 제거됐어요.')
  } catch {
    alert('찜하기 처리에 실패했어요. 다시 시도해주세요.')
  }
}

async function selectProduct() {
  if (!product.value) return
  try {
    await api.post('/api/v1/enrollments/', {
      product_id: product.value.id,
      monthly_amount: goalStore.monthlyAmount * 10000,
      term_months: goalStore.period,
      intr_rate_type: product.value.intr_rate_type,
      rsrv_type: product.value.rsrv_type,
      transfer_day: 25,
      enrolled_at: new Date().toISOString().split('T')[0],
    })
    router.push({ name: 'mypage' })
  } catch {
    alert('상품 가입에 실패했어요. 다시 시도해주세요.')
  }
}
</script>
