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
      <span class="text-2xl font-semibold text-slate-900 pb-8">목표 설정</span>
      <span class="text-base font-medium text-slate-400"
        >{{ step }}단계 · {{ step === 1 ? '기간 선택' : '월 저축 금액 선택' }}</span
      >
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
          <h1 class="text-3xl font-extrabold text-slate-900">언제까지 모을까요?</h1>
          <p class="mt-2 text-slate-500">모으고 싶은 기간을 선택해주세요</p>
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
            매달 얼마를<br />저축할 수 있나요?
          </h1>
          <p class="mt-2 text-slate-500">가능한 금액을 선택하면 예상 수령액을 확인할 수 있어요.</p>
        </div>

        <div class="rounded-2xl border border-slate-200 bg-white p-6">
          <p class="text-base text-slate-500">월 저축 금액</p>
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
          <p class="text-base text-slate-800 pb-1">{{ selectedPeriod }}개월 후 예상 수령액</p>
          <p class="mt-1 text-4xl font-extrabold text-blue-600">{{ totalAmount }}만원</p>
          <div class="mt-4 flex items-center gap-2 text-base">
            <span class="text-slate-500">원금</span>
            <span class="font-bold text-slate-900">{{ principal }}만원</span>
            <span class="text-slate-300">|</span>
            <span class="text-slate-500"
              >예상 이자 <span class="text-sm text-slate-400">세후</span></span
            >
            <span class="font-bold text-blue-600">+{{ afterTaxInterest }}만원</span>
          </div>
          <p class="mt-4 text-sm text-slate-400">
            * 다음 단계에서 우대금리 적용 여부를 직접 확인할 수 있어요.
          </p>
        </div>
      </template>
    </div>

    <!-- 하단 버튼 -->
    <div class="px-5 pb-8 pt-4">
      <button
        @click="onNext"
        :disabled="isLoading"
        class="w-full rounded-2xl bg-blue-600 py-4 text-lg font-semibold text-white transition hover:bg-blue-500 disabled:opacity-60"
      >
        {{ isLoading ? '저장 중...' : step === 1 ? '다음' : '추천 상품 보기' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import api from '@/api/index'

const router = useRouter()
const step = ref(1)
const selectedPeriod = ref(12)
const monthlyAmount = ref(50)
const isLoading = ref(false)
const goalStore = useGoalStore()

const periodOptions = [
  { value: 3, label: '3개월', desc: '빠르게 모으기' },
  { value: 6, label: '6개월', desc: '단기 목표' },
  { value: 12, label: '12개월', desc: '균형 있게 모으기 (가장 인기🔥)' },
  { value: 24, label: '24개월', desc: '여유 있게 모으기' },
  { value: 36, label: '36개월', desc: '장기 플랜' },
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

const onNext = async () => {
  if (step.value === 1) {
    step.value++
  } else {
    isLoading.value = true
    try {
      await api.post('/api/v1/goals/', {
        term_months: selectedPeriod.value,
        monthly_cap: monthlyAmount.value * 10000,
      })
      goalStore.setGoal(selectedPeriod.value, monthlyAmount.value)
      router.push({ name: 'recommendation' })
    } catch {
      alert('목표 저장에 실패했어요. 다시 시도해주세요.')
    } finally {
      isLoading.value = false
    }
  }
}
</script>
