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
        <p
          @click="showLevelGuide = true"
          class="mt-3 cursor-pointer text-base text-slate-400 hover:text-slate-600 transition"
        >
          ⓘ 조건 난이도가 궁금하다면 우대금리 안내를 확인해보세요.
        </p>
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

          <h2 class="text-3xl font-bold text-slate-900">우대금리 조건 안내</h2>
          <p class="mt-2 text-base text-slate-500">조건을 얼마나 쉽게 채울 수 있는지 알려드려요.</p>

          <div class="mt-7 flex gap-2">
            <button
              v-for="level in levelKeys"
              :key="level"
              @click="activeLevelTab = level"
              class="rounded-full px-5 py-2 text-base font-semibold transition"
              :class="
                activeLevelTab === level
                  ? levelMeta[level].activeClass
                  : 'text-slate-400 hover:bg-slate-100'
              "
            >
              {{ level }}
            </button>
          </div>

          <div class="mt-5 rounded-2xl p-5" :class="levelMeta[activeLevelTab].bgClass">
            <div class="flex items-center gap-4">
              <span class="text-4xl">{{ levelMeta[activeLevelTab].icon }}</span>
              <div>
                <span
                  class="rounded-full px-3 py-1 text-sm font-bold"
                  :class="levelMeta[activeLevelTab].badgeClass"
                >
                  {{ levelInfo[activeLevelTab].label }}
                </span>
                <h3 class="mt-1.5 text-xl font-bold text-slate-900">
                  {{ levelInfo[activeLevelTab].title }}
                </h3>
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

      <div v-if="isLoading" class="mt-10 text-center text-slate-400">불러오는 중...</div>

      <!-- 상품 리스트 -->
      <div>
        <p v-if="!isLoading" class="mb-3 text-sm text-slate-400 text-right">
          {{ products.length }}개 · 수령액 높은 순
        </p>
        <div v-if="!isLoading" class="flex flex-col gap-3">
          <ProductCard
            v-for="(product, index) in products"
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
import { ref, computed, onMounted } from 'vue'
import api from '@/api/index'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import { levelInfo } from '@/constants/levelInfo'
import FilterChips from '@/components/Recommendation/FilterChips.vue'
import ProductCard from '@/components/Recommendation/ProductCard.vue'
import { difficultyMap } from '@/constants/difficultyMap'
import { bankColorMap } from '@/constants/bankColors'

const router = useRouter()
const goalStore = useGoalStore()
const showLevelGuide = ref(false)
type LevelKey = 'LOW' | 'MID' | 'HIGH'
const levelKeys: LevelKey[] = ['LOW', 'MID', 'HIGH']
const activeLevelTab = ref<LevelKey>('LOW')
const selectedFilter = ref<'BASE' | 'LOW' | 'MID' | 'HIGH'>('LOW')

const rawProducts = ref<any[]>([])
const isLoading = ref(false)

function resolveMaxDiff(rbd: any, filter: string): string {
  if (!rbd || filter === 'BASE') return ''
  const lowCount = rbd.LOW?.condition_ids?.length ?? 0
  const midCount = rbd.MID?.condition_ids?.length ?? 0
  const highCount = rbd.HIGH?.condition_ids?.length ?? 0
  if (filter === 'LOW') return lowCount > 0 ? 'LOW' : ''
  if (filter === 'MID') {
    if (midCount > lowCount) return 'MID'
    return lowCount > 0 ? 'LOW' : ''
  }
  if (filter === 'HIGH') {
    if (highCount > midCount) return 'HIGH'
    if (midCount > lowCount) return 'MID'
    return lowCount > 0 ? 'LOW' : ''
  }
  return ''
}

const products = computed(() =>
  rawProducts.value.map((item: any) => {
    const levelData = item.rate_by_difficulty?.[selectedFilter.value]
    const maxDiff = resolveMaxDiff(item.rate_by_difficulty, selectedFilter.value)

    return {
      id: item.product_id,
      bankName: item.bank_name,
      bankColor: bankColorMap[item.bank_name] ?? '#6366f1',
      productName: item.product_name,
      baseRate: item.base_rate,
      maxRate: levelData?.expected_rate ?? item.base_rate,
      amount: Math.round((levelData?.expected_payout ?? 0) / 10000),
      difficulty: (!maxDiff ? '없음' : (difficultyMap[maxDiff] ?? '쉬움')) as '없음' | '쉬움' | '보통' | '어려움',
      condition: levelData?.summary_label ? [levelData.summary_label] : [],
    }
  }),
)

const levelMeta: Record<
  LevelKey,
  { icon: string; bgClass: string; badgeClass: string; activeClass: string; dotClass: string }
> = {
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

const fetchProducts = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/v1/products/recommend/', {
      params: {
        term: goalStore.period,
        monthly_cap: goalStore.monthlyAmount * 10000,
      },
    })
    rawProducts.value = data.results
  } catch {
    alert('상품 목록을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => fetchProducts())
</script>
