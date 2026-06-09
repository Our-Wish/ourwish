<template>
  <div class="min-h-screen">
    <header class="pb-8 text-center">
      <span class="text-2xl font-semibold text-slate-900">상품 맞춤 추천</span>
    </header>

    <div class="mx-auto max-w-5xl px-5">
      <div class="relative rounded-3xl bg-blue-500 p-7 text-white">
        <div class="flex items-center justify-between">
          <p class="text-sm font-medium opacity-80">나의 적금 플랜</p>
          <button
            @click="router.go(-1)"
            class="rounded-full bg-white/20 px-4 py-1.5 text-xs font-medium hover:bg-white/30"
          >
            나의 목표 수정하기
          </button>
        </div>
        <p class="mt-4 text-sm opacity-80">
          {{ goalStore.period }}개월간 매달
          <span class="font-bold text-white">{{ goalStore.monthlyAmount }}만원</span>씩 모으면
        </p>
        <p class="mt-1 text-5xl font-extrabold">약 {{ totalAmount }}만원</p>
        <p class="mt-2 text-xs opacity-70">최대 수령 가능 금액 (평균 금리 3.5% 기준)</p>
      </div>

      <div class="mt-3 rounded-2xl border border-slate-200 bg-white p-5">
        <div
          class="flex cursor-pointer items-center justify-between"
          @click="showDetail = !showDetail"
        >
          <span class="font-semibold text-slate-900">💡 우대금리란?</span>
          <span class="text-sm text-slate-400">{{ showDetail ? '닫기 ›' : '자세히 ›' }}</span>
        </div>

        <div v-if="showDetail" class="mt-4 space-y-3 border-t border-slate-100 pt-4">
          <p class="text-sm leading-relaxed text-slate-500">
            특정 조건(급여이체·자동이체 등)을 채워야 추가로 받는 금리예요. 조건이 까다로우면
            <strong class="text-slate-700">기본금리만 보는 것</strong>도 좋은 선택!
          </p>

          <div class="rounded-xl bg-blue-50 p-3 text-sm text-blue-700">
            💬 Tip. 사회초년생이라면 급여이체 + 자동이체 조건이 가장 달성하기 쉬워요!
          </div>
        </div>
      </div>

      <div class="mt-6">
        <FilterChips v-model="selectedFilter" />
      </div>

      <!-- 상품 리스트 -->
      <div class="mt-4">
        <p class="mb-3 text-sm text-slate-400">{{ filteredProducts.length }}개 · 수령액 높은 순</p>
        <div class="flex flex-col gap-3">
          <ProductCard
            v-for="(product, index) in filteredProducts"
            :key="product.id"
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
import FilterChips from '@/components/Recommendation/FilterChips.vue'
import ProductCard from '@/components/Recommendation/ProductCard.vue'

const router = useRouter()
const goalStore = useGoalStore()
const showDetail = ref(false)
const selectedFilter = ref<'BASE' | 'LOW' | 'MID' | 'HIGH'>('LOW')

const totalAmount = computed(() => {
  const { period, monthlyAmount } = goalStore
  const principal = period * monthlyAmount
  const interest = ((monthlyAmount * period * (period + 1)) / 2) * (0.035 / 12)
  return Math.round(principal + interest * (1 - 0.154))
})

type FilterKey = 'BASE' | 'LOW' | 'MID' | 'HIGH'
const filterOrder: FilterKey[] = ['BASE', 'LOW', 'MID', 'HIGH']

const mockProducts = [
  { id: 1, bankName: '하나은행', bankColor: '#00903F', productName: '청년도약 적금', difficulty: '어려움' as const, level: 'HIGH' as FilterKey, amount: 614, maxRate: 5.0, baseRate: 3.5, condition: '소득증빙 + 36개월 유지' },
  { id: 2, bankName: '신한은행', bankColor: '#0046FF', productName: '신한 첫 월급 적금', difficulty: '어려움' as const, level: 'HIGH' as FilterKey, amount: 612, maxRate: 4.5, baseRate: 3.2, condition: '급여이체 + 체크카드 월 30만원 이상' },
  { id: 3, bankName: '국민은행', bankColor: '#FFCD00', productName: 'KB 청춘적금', difficulty: '보통' as const, level: 'MID' as FilterKey, amount: 608, maxRate: 4.0, baseRate: 3.0, condition: '자동이체 + 앱 로그인' },
  { id: 4, bankName: '우리은행', bankColor: '#0F6EBF', productName: '우리 첫 거래 적금', difficulty: '쉬움' as const, level: 'LOW' as FilterKey, amount: 605, maxRate: 3.8, baseRate: 3.2, condition: '신규 고객 + 자동이체 1건' },
  { id: 5, bankName: '농협은행', bankColor: '#00A650', productName: 'NH 디딤돌 정기적금', difficulty: '쉬움' as const, level: 'BASE' as FilterKey, amount: 602, maxRate: 3.6, baseRate: 3.6, condition: '없음' },
]

const filteredProducts = computed(() => {
  const currentIndex = filterOrder.indexOf(selectedFilter.value)
  return mockProducts.filter(p => filterOrder.indexOf(p.level) <= currentIndex)
})
</script>
