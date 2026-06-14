<template>
  <div class="min-h-screen bg-slate-50 pb-10">
    <header class="flex items-center px-5 py-4">
      <button @click="router.go(-1)" class="flex items-center gap-1 text-base text-slate-600">
        <span>‹</span>
        <span>뒤로</span>
      </button>
    </header>

    <div class="px-5 pt-2">
      <h1 class="mt-1 text-3xl font-extrabold text-slate-900">
        <template v-if="goalStore.targetAmount">
          목표를 향해 <span class="text-blue-500">{{ progressPercent }}%</span> 진행중이에요!
        </template>
        <template v-else>목표를 설정해봐요!</template>
      </h1>

      <!-- 목표 카드 (다크) -->
      <GoalCard class="mt-5" :currentSavings="currentSavings" />

      <!-- 통계 행 -->
      <div class="mt-4 grid grid-cols-3 gap-3">
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-sm text-slate-400">가입 상품</p>
          <p class="mt-1 text-xl font-bold text-slate-900">{{ subscribedCount }}개</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-sm text-slate-400">이번 달 납입</p>
          <p class="mt-1 text-xl font-bold text-slate-900">{{ monthlyPayment }}만원</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-sm text-slate-400">빠른 만기</p>
          <p class="mt-1 text-xl font-bold text-slate-900">D-{{ nearestMaturity }}</p>
        </div>
      </div>

      <!-- 진행 중인 적금 -->
      <div class="mt-10">
        <div class="flex items-center justify-between">
          <h2 class="text-2xl font-bold text-slate-900">진행 중인 적금</h2>
          <button
            @click="router.push({ name: 'recommendation' })"
            class="rounded-full bg-slate-100 px-3 py-1.5 text-base font-medium text-slate-600 hover:bg-slate-200 transition"
          >
            + 적금 추가하기
          </button>
        </div>

        <!-- 적금 카드 목록 -->
        <SavingsCard
          v-for="product in savingsStore.myProducts"
          :key="product.id"
          class="mt-3"
          :bankInitial="product.bankName[0] ?? ''"
          :bankColor="product.bankColor"
          :bankName="product.bankName"
          :productName="product.productName"
          :dDay="product.dDay"
          :currentAmount="product.currentAmount"
          :maturityAmount="product.maturityAmount"
          :progress="product.progress"
          :nextPaymentDate="product.nextPaymentDate"
          :monthlyAmount="product.monthlyAmount"
        />
        <p v-if="savingsStore.myProducts.length === 0" class="mt-2 text-base text-slate-400">
          아직 가입한 적금이 없어요 :(
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import GoalCard from '@/components/MyPage/GoalCard.vue'
import SavingsCard from '@/components/MyPage/SavingsCard.vue'
import { useSavingsStore } from '@/stores/savings'

const router = useRouter()
const goalStore = useGoalStore()
const savingsStore = useSavingsStore()

// 나중에 백엔드 연동 예정
const currentSavings = 1000000

const progressPercent = computed(() => {
  if (!goalStore.targetAmount) return 0
  return Math.min(100, Math.round((currentSavings / (goalStore.targetAmount * 10000)) * 100))
})
const subscribedCount = 3
const monthlyPayment = 105
const nearestMaturity = 124
</script>
