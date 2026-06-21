<template>
  <div class="min-h-screen bg-slate-100">
    <div v-if="isLoading" class="flex items-center justify-center py-24 text-slate-400">
      불러오는 중...
    </div>

    <div v-else-if="product" class="mx-auto max-w-6xl px-8 pb-16 pt-2">
      <div class="flex items-start gap-5">
        <div class="w-3/5 space-y-4">
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <div class="flex items-center justify-between gap-6">
              <div class="flex items-center gap-4">
                <div
                  class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full text-xl font-extrabold text-white"
                  :style="{ backgroundColor: product.bankColor }"
                >
                  {{ product.bankName[0] }}
                </div>
                <div>
                  <p class="text-sm text-slate-400">{{ product.bankName }} · 적금</p>
                  <p class="mt-0.5 text-xl font-bold text-slate-900">{{ product.productName }}</p>
                  <p class="mt-1 text-sm text-slate-500">
                    예상 세후 수령액
                    <span class="font-bold text-slate-900">{{ estimatedAmount }}만원</span>
                  </p>
                </div>
              </div>

              <!-- 금리 -->
              <div class="text-center">
                <p class="text-sm text-slate-400">최고 금리</p>
                <p class="mt-1 text-4xl font-extrabold text-blue-600">연 {{ product.maxRate }}%</p>
                <p class="mt-0.5 text-sm text-slate-400">기본금리 {{ product.baseRate }}%</p>
              </div>

              <!-- 버튼 -->
              <div class="flex flex-col items-end gap-2">
                <a href="#" class="text-sm text-slate-400 hover:text-slate-600">상품 보러가기 →</a>
                <button
                  @click="selectProduct"
                  class="rounded-xl bg-blue-500 px-6 py-2.5 text-base font-semibold text-white transition hover:bg-blue-400"
                >
                  상품 등록하기
                </button>
                <button
                  @click="isFavorite = !isFavorite"
                  class="rounded-xl border px-6 py-2.5 text-base font-semibold transition"
                  :class="
                    isFavorite
                      ? 'border-blue-400 bg-blue-50 text-blue-600'
                      : 'border-slate-300 text-slate-600 hover:border-slate-400'
                  "
                >
                  {{ isFavorite ? '찜 완료 ♥' : '상품 찜하기' }}
                </button>
              </div>
            </div>
          </div>

          <!-- 상품 기본 정보 -->
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <p class="text-base font-bold text-slate-900">상품 기본 정보</p>
            <div class="mt-3 divide-y divide-slate-100">
              <div
                v-for="item in product.conditions"
                :key="item.label"
                class="flex items-center gap-3 py-2.5"
              >
                <div
                  class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-50"
                >
                  <svg
                    class="h-3.5 w-3.5 text-blue-400"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      v-if="item.label === '가입 대상'"
                      d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                    />
                    <path
                      v-else-if="item.label === '가입 방법'"
                      d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 8.25h3m-3 3h3m-6 3h.008v.008H6.75V15z"
                    />
                    <path
                      v-else-if="item.label === '월 납입 한도'"
                      d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"
                    />
                    <path
                      v-else-if="item.label === '만기후 이자율'"
                      d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                    <path
                      v-else
                      d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
                    />
                  </svg>
                </div>
                <span class="w-24 shrink-0 text-sm font-medium text-blue-500">{{
                  item.label
                }}</span>
                <span class="text-sm text-slate-700">{{ item.value }}</span>
              </div>
            </div>
            <p class="mt-4 text-sm text-slate-400">
              ※ 자세한 내용은 상품설명서 및 약관을 확인해주세요.
            </p>
          </div>

          <!-- 우대금리 조건 -->
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <div class="flex items-center gap-2">
              <p class="text-base font-bold text-slate-900">우대금리 조건</p>
              <span
                v-if="product.bonusConditions.length"
                class="rounded-full bg-blue-100 px-2.5 py-0.5 text-sm font-semibold text-blue-600"
                >{{ product.bonusConditions.length }}개</span
              >
            </div>

            <div v-if="product.bonusConditions.length" class="mt-4 divide-y divide-slate-100">
              <div
                v-for="(cond, index) in product.bonusConditions"
                :key="cond.label"
                class="flex cursor-pointer items-center gap-4 py-3.5"
                @click="toggleCondition(index)"
              >
                <div
                  class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md border-2 transition"
                  :class="
                    checked[index] ? 'border-blue-500 bg-blue-500' : 'border-slate-300 bg-white'
                  "
                >
                  <svg
                    v-if="checked[index]"
                    class="h-3 w-3 text-white"
                    viewBox="0 0 12 12"
                    fill="none"
                  >
                    <path
                      d="M2 6l3 3 5-5"
                      stroke="currentColor"
                      stroke-width="2"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    />
                  </svg>
                </div>
                <span class="flex-1 text-base text-slate-800">{{ cond.label }}</span>
                <span
                  class="shrink-0 rounded-full px-2.5 py-0.5 text-sm font-semibold"
                  :class="difficultyBadgeClass[cond.difficulty] ?? 'bg-slate-100 text-slate-500'"
                  >{{ difficultyLabel[cond.difficulty] ?? cond.difficulty }}</span
                >
                <span class="shrink-0 text-base font-semibold text-blue-400"
                  >+{{ cond.bonusRate.toFixed(1) }}%p</span
                >
              </div>
            </div>
            <p v-else class="mt-4 text-base text-slate-400">우대 조건이 없는 상품이에요</p>

            <!-- 금리 계산 결과 -->
            <div class="mt-5 rounded-xl bg-blue-50 px-5 py-4">
              <p class="text-sm text-blue-400">현재 예상 금리</p>
              <p class="mt-1 text-3xl font-extrabold text-blue-600">
                연 {{ currentRate.toFixed(2) }}%
              </p>
              <div class="mt-3 flex items-end justify-between">
                <div>
                  <p class="text-sm text-slate-400">예상 세후 수령액</p>
                  <p class="mt-0.5 text-xl font-bold text-slate-900">{{ estimatedAmount }}만원</p>
                </div>
                <p class="text-sm text-slate-400">
                  매달 {{ goalStore.monthlyAmount }}만원 · {{ goalStore.period }}개월
                </p>
              </div>
            </div>
          </div>

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
        </div>

        <!-- ── 오른쪽 (2/5) ── -->
        <div class="w-2/5 space-y-4">
          <!-- 근처 영업점 -->
          <div class="rounded-2xl bg-white p-5 shadow-sm">
            <p class="text-base font-bold text-slate-900">근처 영업점 찾기</p>

            <!-- 카카오맵 자리 -->
            <div
              class="mt-4 flex h-44 items-center justify-center rounded-xl bg-slate-100 text-sm text-slate-400"
            >
              지도 영역 (카카오맵)
            </div>

            <!-- 지점 목록 자리 -->
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
import Chat from '@/components/Chat.vue'

const router = useRouter()
const route = useRoute()
const goalStore = useGoalStore()

const productId = computed(() => Number(route.params.id))

const difficultyBadgeClass: Record<string, string> = {
  LOW: 'bg-green-50 text-green-700',
  MID: 'bg-yellow-50 text-yellow-700',
  HIGH: 'bg-red-50 text-red-600',
}

const difficultyLabel: Record<string, string> = {
  LOW: '쉬움',
  MID: '보통',
  HIGH: '어려움',
}

const checked = ref<boolean[]>([])
const isLoading = ref(false)
const isFavorite = ref(false)

function toggleCondition(index: number) {
  checked.value[index] = !checked.value[index]
}

type Condition = { label: string; value: string }
type BonusCondition = { condition_id: number; label: string; bonusRate: number; difficulty: string }

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
  aiSummaries: string[]
  bonusConditions: BonusCondition[]
}

const product = ref<ProductDetail | null>(null)

function formatLimit(value: number): string {
  if (!value || value > 9e15) return '제한 없음'
  return `${Math.round(value / 10000).toLocaleString()}만원`
}

function buildProduct(data: any): ProductDetail {
  const baseRate = data.base_rate ?? 0
  const maxRate = data.max_rate ?? 0

  const matchedOption =
    (data.options ?? []).find((o: any) => o.save_term === goalStore.period) ??
    data.options?.[0] ??
    {}

  const bonusConditions: BonusCondition[] = (data.conditions ?? []).map((c: any) => ({
    condition_id: c.condition_id,
    label: c.friendly_label || c.label,
    bonusRate: c.rate,
    difficulty: c.difficulty,
  }))

  checked.value = bonusConditions.map(() => false)

  return {
    id: data.product_id,
    bankName: data.bank_name,
    bankColor: bankColorMap[data.bank_name] ?? '#6366f1',
    productName: data.product_name,
    baseRate,
    maxRate,
    intr_rate_type: matchedOption.intr_rate_type ?? 'S',
    rsrv_type: matchedOption.rsrv_type ?? 'S',
    conditions: [
      { label: '가입 대상', value: data.join_member ?? '-' },
      { label: '가입 방법', value: data.join_way ?? '-' },
      { label: '월 납입 한도', value: formatLimit(data.max_limit) },
      { label: '만기후 이자율', value: data.maturity_interest ?? '-' },
      { label: '기타 유의사항', value: data.etc_note ?? '-' },
    ],
    aiSummaries: [data.join_summary, data.maturity_summary, data.etc_summary].filter(Boolean),
    bonusConditions,
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    const { data } = await api.get(`/api/v1/products/${productId.value}/`)
    product.value = buildProduct(data)
  } catch {
    alert('상품 정보를 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
})

const currentRate = computed(() => {
  if (!product.value) return 0
  const bonus = product.value.bonusConditions.reduce(
    (sum, cond, i) => (checked.value[i] ? sum + cond.bonusRate : sum),
    0,
  )
  return product.value.baseRate + bonus
})

const estimatedAmount = computed(() => {
  const { period, monthlyAmount } = goalStore
  const rate = currentRate.value / 100
  const interest = ((monthlyAmount * period * (period + 1)) / 2) * (rate / 12)
  return Math.round(period * monthlyAmount + interest * (1 - 0.154))
})

async function selectProduct() {
  if (!product.value) return
  const checkedConditionIds = product.value.bonusConditions
    .filter((_, i) => checked.value[i])
    .map((c) => c.condition_id)

  try {
    await api.post('/api/v1/enrollments/', {
      product_id: product.value.id,
      monthly_amount: goalStore.monthlyAmount * 10000,
      term_months: goalStore.period,
      intr_rate_type: product.value.intr_rate_type,
      rsrv_type: product.value.rsrv_type,
      transfer_day: 25,
      enrolled_at: new Date().toISOString().split('T')[0],
      checked_condition_ids: checkedConditionIds,
    })
    router.push({ name: 'mypage' })
  } catch {
    alert('상품 가입에 실패했어요. 다시 시도해주세요.')
  }
}
</script>
