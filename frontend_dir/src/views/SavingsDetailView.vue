<template>
  <div class="min-h-screen bg-slate-50 pb-24">
    <header class="flex items-center px-5 py-4">
      <button @click="router.go(-1)" class="flex items-center gap-1 text-sm text-slate-600">
        <span>‹</span>
        <span>뒤로</span>
      </button>
    </header>

    <div v-if="isLoading" class="flex items-center justify-center py-24 text-slate-400">
      불러오는 중...
    </div>

    <div v-else-if="product" class="px-5 pb-12">
      <!-- 상단 카드 -->
      <div class="rounded-3xl p-6 text-white" :style="{ backgroundColor: product.bankColor }">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div
              class="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 text-sm font-bold"
            >
              {{ product.bankName[0] }}
            </div>
            <span class="text-sm font-medium opacity-90">{{ product.bankName }} · 적금</span>
          </div>
          <span class="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold">★ 우대금리</span>
        </div>

        <h1 class="mt-5 text-2xl font-bold">{{ product.productName }}</h1>

        <div class="my-4 border-t border-white/20" />

        <div class="flex items-end justify-between">
          <div>
            <p class="text-xs opacity-70">현재 예상 금리</p>
            <p class="mt-1 text-4xl font-extrabold">약 {{ product.baseRate.toFixed(2) }}%</p>
          </div>
          <div class="text-right text-sm opacity-90">
            <p class="opacity-70">기본/최고</p>
            <p class="font-semibold">{{ product.baseRate }}% / {{ product.maxRate }}%</p>
          </div>
        </div>

        <div
          class="mt-4 flex w-full items-center justify-between rounded-2xl bg-white/15 px-4 py-3 text-sm font-medium"
        >
          <span>{{ product.bankName }} · {{ product.productName }}</span>
        </div>
      </div>

      <!-- 핵심 조건 -->
      <div class="mt-8">
        <p class="text-sm font-semibold text-blue-500">핵심 조건</p>
        <p class="mt-1 text-lg font-bold text-slate-900">한눈에 보는 상세 내용</p>

        <div class="mt-4 overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div
            v-for="(item, index) in product.conditions"
            :key="item.label"
            class="flex items-start gap-6 px-5 py-4"
            :class="{ 'border-t border-slate-100': index > 0 }"
          >
            <span class="w-24 shrink-0 text-sm text-slate-400">{{ item.label }}</span>
            <span class="text-sm font-semibold text-slate-900">{{ item.value }}</span>
          </div>
        </div>
      </div>

      <!-- AI 쉽게 풀어쓴 설명 -->
      <div class="mt-6 rounded-2xl bg-slate-100 p-5">
        <div class="flex items-center gap-2">
          <span class="rounded-lg bg-indigo-500 px-2 py-0.5 text-xs font-bold text-white">AI</span>
          <span class="text-sm font-semibold text-indigo-500">쉽게 풀어쓴 설명</span>
        </div>
        <p class="mt-3 font-bold text-slate-900">{{ product.aiHeadline }}</p>
        <p class="mt-1 text-sm text-slate-500">{{ product.aiDescription }}</p>
      </div>

      <!-- 나의 금리 알아보기 -->
      <div class="mt-8">
        <p class="text-sm font-semibold text-blue-500">나의 금리 알아보기</p>
        <p class="mt-1 text-lg font-bold text-slate-900">달성할 수 있는 조건을 체크해보세요</p>
        <p class="mt-0.5 text-xs text-slate-400">
          체크한 조건에 따라 예상 금리·세후수령액이 바뀌어요
        </p>

        <!-- 체크박스 목록 -->
        <div class="mt-4 overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div
            v-for="(cond, index) in product.bonusConditions"
            :key="cond.label"
            class="flex cursor-pointer items-center gap-4 px-5 py-4"
            :class="{ 'border-t border-slate-100': index > 0 }"
            @click="toggleCondition(index)"
          >
            <div
              class="flex h-5 w-5 shrink-0 items-center justify-center rounded-md border-2 transition"
              :class="checked[index] ? 'border-blue-500 bg-blue-500' : 'border-slate-300 bg-white'"
            >
              <svg v-if="checked[index]" class="h-3 w-3 text-white" viewBox="0 0 12 12" fill="none">
                <path
                  d="M2 6l3 3 5-5"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
            <span class="flex-1 text-sm text-slate-800">{{ cond.label }}</span>
            <span class="text-sm font-semibold text-slate-400"
              >+{{ cond.bonusRate.toFixed(1) }}%p</span
            >
          </div>
        </div>

        <!-- 결과 영역 -->
        <div class="mt-3 rounded-2xl border border-slate-200 bg-white px-5 py-5">
          <p class="text-xs text-slate-400">현재 예상 금리</p>
          <p class="mt-1 text-3xl font-extrabold text-blue-600">연 {{ currentRate.toFixed(2) }}%</p>

          <div class="mt-4 flex items-end justify-between">
            <div>
              <p class="text-xs text-slate-400">예상 세후 수령액</p>
              <p class="mt-1 text-xl font-bold text-slate-900">{{ estimatedAmount }}만원</p>
            </div>
            <p class="text-xs text-slate-400">
              매달 {{ goalStore.monthlyAmount }}만원 · {{ goalStore.period }}개월
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- 하단 고정 버튼 -->
    <div class="mx-auto max-w-6xl px-9">
      <button
        @click="selectProduct"
        class="w-full rounded-2xl bg-blue-500 py-3 text-lg font-semibold text-white transition hover:bg-blue-400"
      >
        이 상품 선택하기
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import { useSavingsStore } from '@/stores/savings'
import api from '@/api/index'
import { bankColorMap } from '@/constants/bankColors'

const router = useRouter()
const route = useRoute()
const goalStore = useGoalStore()
const savingsStore = useSavingsStore()

const productId = computed(() => Number(route.params.id))

const checked = ref<boolean[]>([])
const isLoading = ref(false)

function toggleCondition(index: number) {
  checked.value[index] = !checked.value[index]
}

type Condition = { label: string; value: string }
type BonusCondition = { label: string; bonusRate: number }

type ProductDetail = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  baseRate: number
  maxRate: number
  conditions: Condition[]
  aiHeadline: string
  aiDescription: string
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
  const bonusRate = Math.max(0, maxRate - baseRate)

  // TODO: 우대금리 개별 조건 API 연동 필요
  const bonusConditions: BonusCondition[] =
    data.has_bonus && bonusRate > 0 ? [{ label: '우대금리 조건 달성', bonusRate }] : []

  checked.value = bonusConditions.map(() => false)

  const summaryParts = [data.join_summary, data.maturity_summary, data.etc_summary].filter(Boolean)

  return {
    id: data.product_id,
    bankName: data.bank_name,
    bankColor: bankColorMap[data.bank_name] ?? '#94a3b8',
    productName: data.product_name,
    baseRate,
    maxRate,
    conditions: [
      { label: '가입 대상', value: data.join_member ?? '-' },
      { label: '가입 방법', value: data.join_way ?? '-' },
      { label: '월 납입 한도', value: formatLimit(data.max_limit) },
      { label: '만기후 이자율', value: data.maturity_interest ?? '-' },
      { label: '기타 유의사항', value: data.etc_note ?? '-' },
    ],
    aiHeadline: summaryParts[0] ?? '',
    aiDescription: summaryParts.slice(1).join(' ') ?? '',
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

function selectProduct() {
  if (!product.value) return
  savingsStore.addProduct({
    id: product.value.id,
    bankName: product.value.bankName,
    bankColor: product.value.bankColor,
    productName: product.value.productName,
    dDay: goalStore.period * 30,
    currentAmount: 0,
    maturityAmount: estimatedAmount.value,
    progress: 0,
    nextPaymentDate: '다음 달 25일',
    monthlyAmount: goalStore.monthlyAmount,
  })
  router.push({ name: 'mypage' })
}
</script>
