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
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import FilterChips from '@/components/Recommendation/FilterChips.vue'

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
</script>
