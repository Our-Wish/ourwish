<template>
  <div class="flex min-h-screen flex-col bg-slate-50">
    <!-- 상단 헤더 -->
    <header class="flex items-center justify-between px-5 py-4">
      <button
        @click="onBack"
        class="flex h-9 w-9 items-center justify-center rounded-full hover:bg-slate-100"
      >
        <svg
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M15 18l-6-6 6-6" />
        </svg>
      </button>
      <span class="text-xl font-semibold text-slate-900 pb-8">목표 설정</span>
      <span class="text-sm font-medium text-slate-400">{{ step }}/2</span>
    </header>

    <!-- 프로그레스 바 -->
    <div class="flex gap-1.5 px-5">
      <div
        class="h-1.5 flex-1 rounded-full transition-colors"
        :class="step >= 1 ? 'bg-blue-600' : 'bg-slate-200'"
      />
      <div
        class="h-1.5 flex-1 rounded-full transition-colors"
        :class="step >= 2 ? 'bg-blue-600' : 'bg-slate-200'"
      />
    </div>

    <!-- 콘텐츠 -->
    <div class="flex flex-1 flex-col px-5 pt-10">
      <!-- Step 1: 기간 선택 -->
      <template v-if="step === 1">
        <div class="mb-8">
          <h1 class="text-3xl font-extrabold text-slate-900">얼마나 모을까요?</h1>
          <p class="mt-2 text-slate-500">기간을 정해주세요</p>
        </div>

        <div class="flex flex-col gap-3">
          <button
            v-for="option in periodOptions"
            :key="option.value"
            @click="selectedPeriod = option.value"
            class="flex items-center justify-between rounded-2xl border-2 px-6 py-5 text-left transition"
            :class="
              selectedPeriod === option.value
                ? 'border-blue-600 bg-blue-50'
                : 'border-slate-200 bg-white hover:border-slate-300'
            "
          >
            <div>
              <p class="text-xl font-bold text-slate-900">{{ option.label }}</p>
              <p class="mt-0.5 text-sm text-slate-400">{{ option.desc }}</p>
            </div>
            <div
              v-if="selectedPeriod === option.value"
              class="flex h-7 w-7 items-center justify-center rounded-full bg-blue-600"
            >
              <svg
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                stroke-width="3"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M20 6L9 17l-5-5" />
              </svg>
            </div>
          </button>
        </div>
      </template>

      <!-- Step 2: 월 납입액 -->
      <template v-if="step === 2">
        <div class="mb-8">
          <h1 class="text-3xl font-extrabold leading-tight text-slate-900">
            매달 얼마까지<br />납입 가능해요?
          </h1>
          <p class="mt-2 text-slate-500">슬라이더를 움직이면 예상 금액이 보여요</p>
        </div>

        <div class="rounded-2xl border border-slate-200 bg-white p-6">
          <p class="text-sm text-slate-400">매달 납입할 금액</p>
          <p class="mt-1 text-4xl font-extrabold text-slate-900">{{ monthlyAmount }}만원</p>

          <div class="mt-6">
            <input
              v-model.number="monthlyAmount"
              type="range"
              :min="5"
              :max="300"
              :step="5"
              class="w-full accent-blue-600"
            />
            <div class="mt-1 flex justify-between text-xs text-slate-400">
              <span>5만원</span>
              <span>300만원</span>
            </div>
          </div>

          <div class="mt-5 flex flex-wrap gap-2">
            <button
              v-for="chip in amountChips"
              :key="chip"
              @click="monthlyAmount = chip"
              class="rounded-full px-4 py-1.5 text-sm font-medium transition"
              :class="
                monthlyAmount === chip
                  ? 'bg-blue-600 text-white'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              "
            >
              {{ chip }}만원
            </button>
          </div>
        </div>

        <!-- 예상 금액 카드 -->
        <div class="mt-4 rounded-2xl border border-slate-200 bg-white p-6">
          <p class="text-sm text-slate-400">{{ selectedPeriod }}개월 후 예상</p>
          <p class="mt-1 text-4xl font-extrabold text-blue-600">약 {{ totalAmount }}만원</p>
          <div class="mt-4 flex items-end justify-between">
            <div>
              <p class="text-xs text-slate-400">원금</p>
              <p class="mt-0.5 font-semibold text-slate-900">{{ principal }}만원</p>
            </div>
            <div class="text-right">
              <p class="text-xs text-slate-400">예상 이자(세후)</p>
              <p class="mt-0.5 font-semibold text-blue-600">+{{ afterTaxInterest }}만원</p>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 하단 버튼 -->
    <div class="px-5 pb-8 pt-4">
      <button
        @click="onNext"
        class="w-full rounded-2xl bg-blue-600 py-4 text-lg font-semibold text-white transition hover:bg-blue-500"
      >
        {{ step === 1 ? '다음' : '추천 받기' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'

const router = useRouter()
const step = ref(1)
const selectedPeriod = ref(12)
const monthlyAmount = ref(50)
const goalStore = useGoalStore()

const periodOptions = [
  { value: 3, label: '3개월', desc: '빠르게 모으기' },
  { value: 6, label: '6개월', desc: '단기 목표' },
  { value: 12, label: '12개월', desc: '가장 인기✨' },
  { value: 24, label: '24개월', desc: '여유롭게 모으기' },
  { value: 36, label: '36개월', desc: '장기 목표' },
]

const amountChips = [10, 30, 50, 100]

// 적금 이자 계산 (연 4.5%, 세후 15.4% 공제)
const principal = computed(() => monthlyAmount.value * selectedPeriod.value)
const afterTaxInterest = computed(() => {
  const interest =
    ((monthlyAmount.value * selectedPeriod.value * (selectedPeriod.value + 1)) / 2) * (0.045 / 12)
  return Math.round(interest * (1 - 0.154))
})
const totalAmount = computed(() => principal.value + afterTaxInterest.value)

const onBack = () => {
  if (step.value === 1) router.push({ name: 'home' })
  else step.value--
}

const onNext = () => {
  if (step.value === 1) step.value++
  else {
    goalStore.setGoal(selectedPeriod.value, monthlyAmount.value)
    router.push({ name: 'recommendation' })
  }
}
</script>
