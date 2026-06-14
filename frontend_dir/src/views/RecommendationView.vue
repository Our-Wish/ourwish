<template>
  <div class="min-h-screen">
    <header class="pb-8 text-center">
      <span class="text-2xl font-semibold text-slate-900">상품 맞춤 추천</span>
    </header>

    <div class="mx-auto max-w-5xl px-5">
      <div
        class="relative overflow-hidden rounded-4xl bg-linear-to-br from-blue-600 via-blue-600 to-indigo-700 px-8 py-8 text-white shadow-2xl shadow-blue-200/70"
      >
        <div
          class="pointer-events-none absolute -right-24 -top-28 h-80 w-80 rounded-full bg-white/15 blur-3xl"
        ></div>
        <div
          class="pointer-events-none absolute -bottom-28 left-1/3 h-72 w-72 rounded-full bg-sky-300/20 blur-3xl"
        ></div>

        <div class="relative z-10 flex items-start justify-between gap-6">
          <div>
            <p class="text-base font-semibold text-blue-100">나의 적금 플랜</p>
          </div>
          <button
            @click="router.go(-1)"
            class="rounded-full bg-white/15 px-5 py-2.5 text-base font-semibold text-white backdrop-blur transition hover:bg-white/25"
          >
            목표 수정하기
          </button>
        </div>

        <div class="relative z-10 mt-3 flex items-end justify-between gap-8">
          <div>
            <p class="text-base font-medium text-blue-100">예상 만기 수령액</p>
            <p class="mt-2 text-6xl font-extrabold tracking-tight text-white">
              약 {{ totalAmount }}만원
            </p>
            <p class="mt-3 text-base font-medium text-blue-100">평균 금리 3.5% 기준</p>
          </div>
          <div class="grid min-w-70 grid-cols-2 gap-3">
            <div class="rounded-2xl bg-white/10 px-5 py-4 backdrop-blur ring-1 ring-white/15">
              <p class="text-base font-medium text-blue-100">기간</p>
              <p class="mt-1 text-2xl font-extrabold text-white">{{ goalStore.period }}개월</p>
            </div>
            <div class="rounded-2xl bg-white/10 px-5 py-4 backdrop-blur ring-1 ring-white/15">
              <p class="text-base font-medium text-blue-100">월 저축</p>
              <p class="mt-1 text-2xl font-extrabold text-white">
                {{ goalStore.monthlyAmount }}만원
              </p>
            </div>
          </div>
        </div>

        <div
          class="relative z-10 mt-7 flex items-center justify-between rounded-2xl bg-white/10 px-5 py-4 backdrop-blur ring-1 ring-white/15"
        >
          <p class="text-base font-medium text-blue-50">
            💡 우대금리 조건에 따라 실제 수령액은 달라질 수 있어요.
          </p>
          <button
            @click="showLevelGuide = true"
            class="flex items-center gap-1 rounded-full bg-white px-4 py-1.5 text-base font-bold text-blue-600 transition hover:bg-blue-50"
          >
            우대금리 난이도 알아보기
          </button>
        </div>
      </div>

      <div class="mt-6">
        <FilterChips v-model="selectedFilter" />
      </div>

      <!-- 레벨 안내 모달 -->
      <div v-if="showLevelGuide" class="fixed inset-0 z-50 flex items-center justify-center p-10">
        <div class="absolute inset-0 bg-slate-950/40" @click="showLevelGuide = false" />
        <div
          class="relative w-full max-w-lg rounded-4xl bg-white pt-12 px-10 shadow-2xl shadow-slate-950/20 max-h-[85vh] overflow-y-auto"
        >
          <button
            @click="showLevelGuide = false"
            class="absolute right-6 top-6 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-400 transition hover:bg-slate-100"
          >
            ✕
          </button>

          <h2 class="text-2xl font-bold text-slate-900">우대금리 조건 안내</h2>
          <p class="mt-2 text-base text-slate-500">조건을 얼마나 쉽게 채울 수 있는지 알려드려요.</p>

          <div class="mt-7 flex gap-2">
            <button
              v-for="level in levelKeys"
              :key="level"
              @click="activeLevelTab = level"
              class="rounded-full px-5 py-2 text-base font-semibold transition"
              :class="activeLevelTab === level ? levelMeta[level].activeClass : 'text-slate-400 hover:bg-slate-100'"
            >
              {{ level }}
            </button>
          </div>

          <div class="mt-5 rounded-2xl p-5" :class="levelMeta[activeLevelTab].bgClass">
            <div class="flex items-center gap-4">
              <span class="text-4xl">{{ levelMeta[activeLevelTab].icon }}</span>
              <div>
                <span class="rounded-full px-3 py-1 text-sm font-bold" :class="levelMeta[activeLevelTab].badgeClass">
                  {{ levelInfo[activeLevelTab].label }}
                </span>
                <h3 class="mt-1.5 text-xl font-bold text-slate-900">{{ levelInfo[activeLevelTab].title }}</h3>
              </div>
            </div>
            <p class="mt-3 text-base text-slate-600">{{ levelInfo[activeLevelTab].description }}</p>
          </div>

          <p class="mt-6 text-base font-semibold text-slate-400">대표적인 우대조건 예시</p>
          <div class="mt-3 space-y-2 pb-10">
            <div
              v-for="condition in levelInfo[activeLevelTab].conditions"
              :key="condition"
              class="flex items-center gap-3 rounded-xl bg-slate-50 px-5 py-3.5 text-base text-slate-700"
            >
              <span class="text-xs" :class="levelMeta[activeLevelTab].dotClass">●</span>
              {{ condition }}
            </div>
          </div>
        </div>
      </div>

      <!-- 상품 리스트 -->
      <div class="mt-4">
        <p class="mb-3 text-sm text-slate-400">{{ filteredProducts.length }}개 · 수령액 높은 순</p>
        <div class="flex flex-col gap-3">
          <ProductCard
            v-for="(product, index) in filteredProducts"
            :key="product.id"
            :id="product.id"
            :rank="index + 1"
            :bank-name="product.bankName"
            :bank-color="product.bankColor"
            :product-name="product.productName"
            :difficulty="product.difficulty"
            :amount="product.amount"
            :max-rate="product.maxRate"
            :base-rate="product.baseRate"
            :condition="product.condition"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import { levelInfo } from '@/constants/levelInfo'
import FilterChips from '@/components/Recommendation/FilterChips.vue'
import ProductCard from '@/components/Recommendation/ProductCard.vue'

const router = useRouter()
const goalStore = useGoalStore()
const showDetail = ref(false)
const showLevelGuide = ref(false)
type LevelKey = 'LOW' | 'MID' | 'HIGH'
const levelKeys: LevelKey[] = ['LOW', 'MID', 'HIGH']
const activeLevelTab = ref<LevelKey>('LOW')
const selectedFilter = ref<'BASE' | 'LOW' | 'MID' | 'HIGH'>('LOW')

const levelMeta: Record<LevelKey, { icon: string; bgClass: string; badgeClass: string; activeClass: string; dotClass: string }> = {
  LOW: {
    icon: '🌿',
    bgClass: 'bg-emerald-50',
    badgeClass: 'bg-emerald-100 text-emerald-700',
    activeClass: 'bg-emerald-500 text-white',
    dotClass: 'text-emerald-400',
  },
  MID: {
    icon: '⚡',
    bgClass: 'bg-amber-50',
    badgeClass: 'bg-amber-100 text-amber-700',
    activeClass: 'bg-amber-500 text-white',
    dotClass: 'text-amber-400',
  },
  HIGH: {
    icon: '🔥',
    bgClass: 'bg-red-50',
    badgeClass: 'bg-red-100 text-red-700',
    activeClass: 'bg-red-500 text-white',
    dotClass: 'text-red-400',
  },
}

const totalAmount = computed(() => {
  const { period, monthlyAmount } = goalStore
  const principal = period * monthlyAmount
  const interest = ((monthlyAmount * period * (period + 1)) / 2) * (0.035 / 12)
  return Math.round(principal + interest * (1 - 0.154))
})

type FilterKey = 'BASE' | 'LOW' | 'MID' | 'HIGH'
const filterOrder: FilterKey[] = ['BASE', 'LOW', 'MID', 'HIGH']

const mockProducts = [
  {
    id: 1,
    bankName: '하나은행',
    bankColor: '#00903F',
    productName: '청년도약 적금',
    difficulty: '어려움' as const,
    level: 'HIGH' as FilterKey,
    amount: 614,
    maxRate: 5.0,
    baseRate: 3.5,
    condition: '소득증빙 + 36개월 유지',
  },
  {
    id: 2,
    bankName: '신한은행',
    bankColor: '#0046FF',
    productName: '신한 첫 월급 적금',
    difficulty: '어려움' as const,
    level: 'HIGH' as FilterKey,
    amount: 612,
    maxRate: 4.5,
    baseRate: 3.2,
    condition: '급여이체 + 체크카드 월 30만원 이상',
  },
  {
    id: 3,
    bankName: '국민은행',
    bankColor: '#FFCD00',
    productName: 'KB 청춘적금',
    difficulty: '보통' as const,
    level: 'MID' as FilterKey,
    amount: 608,
    maxRate: 4.0,
    baseRate: 3.0,
    condition: '자동이체 + 앱 로그인',
  },
  {
    id: 4,
    bankName: '우리은행',
    bankColor: '#0F6EBF',
    productName: '우리 첫 거래 적금',
    difficulty: '쉬움' as const,
    level: 'LOW' as FilterKey,
    amount: 605,
    maxRate: 3.8,
    baseRate: 3.2,
    condition: '신규 고객 + 자동이체 1건',
  },
  {
    id: 5,
    bankName: '농협은행',
    bankColor: '#00A650',
    productName: 'NH 디딤돌 정기적금',
    difficulty: '쉬움' as const,
    level: 'BASE' as FilterKey,
    amount: 602,
    maxRate: 3.6,
    baseRate: 3.6,
    condition: '없음',
  },
]

const filteredProducts = computed(() => {
  const currentIndex = filterOrder.indexOf(selectedFilter.value)
  return mockProducts.filter((p) => filterOrder.indexOf(p.level) <= currentIndex)
})
</script>
