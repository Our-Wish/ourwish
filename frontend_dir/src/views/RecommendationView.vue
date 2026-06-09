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
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'

const router = useRouter()
const goalStore = useGoalStore()

const totalAmount = computed(() => {
  const { period, monthlyAmount } = goalStore
  const principal = period * monthlyAmount
  const interest = ((monthlyAmount * period * (period + 1)) / 2) * (0.035 / 12)
  return Math.round(principal + interest * (1 - 0.154))
})
</script>
