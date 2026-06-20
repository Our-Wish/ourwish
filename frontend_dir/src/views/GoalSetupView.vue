<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-16">
    <div class="flex pl-40">
      <div class="flex w-1/3 flex-col justify-between">
        <div>
          <p class="text-xl font-semibold text-blue-600">
            {{ step === 1 ? 'STEP 01' : 'STEP 02' }}
          </p>
          <h1 class="mt-3 text-5xl font-extrabold leading-tight text-slate-900">
            <template v-if="step === 1">얼마나 모을지<br />먼저 정해볼게요</template>
            <template v-else>받을 수 있는<br />우대조건을 찾아볼게요</template>
          </h1>
          <p class="mt-5 text-lg leading-relaxed text-slate-500">
            <template v-if="step === 1">
              저축 기간과 매달 넣을 금액을 알려주시면<br />목표에 맞는 적금 후보를 찾아드릴게요.
            </template>
            <template v-else>
              실제로 받을 수 있는 금리는 사람마다 달라요.<br />회원님이 받을 수 있는 최적의
              우대금리를 찾아드릴게요.
            </template>
          </p>
        </div>
        <img :src="step === 1 ? hiWish : questionWish" class="mb-10 w-60 self-start" />
      </div>
      <div class="w-px bg-slate-200" />

      <div class="flex flex-1 flex-col justify-between px-16 pt-10">
        <template v-if="step === 1">
          <div class="flex flex-col gap-8">
            <div>
              <p class="mb-4 text-lg font-medium text-slate-700">1. 저축 기간</p>
              <div class="flex gap-3">
                <button
                  v-for="option in periodOptions"
                  :key="option.value"
                  @click="selectedPeriod = option.value"
                  class="flex-1 rounded-2xl border-2 py-3 text-base font-semibold transition"
                  :class="
                    selectedPeriod === option.value
                      ? 'border-slate-900 bg-slate-900 text-white'
                      : 'border-slate-200 bg-white text-slate-700 hover:border-slate-400'
                  "
                >
                  {{ option.label }}
                </button>
              </div>
            </div>

            <div>
              <p class="mb-4 text-lg font-medium text-slate-700">2. 월 저축 금액</p>
              <div class="rounded-2xl border border-slate-200 bg-white/70 px-6 py-5">
                <div class="flex items-center justify-between">
                  <p class="text-2xl font-extrabold text-slate-900">{{ monthlyAmount }}만원</p>
                </div>
                <div class="mt-4">
                  <input
                    v-model.number="monthlyAmount"
                    type="range"
                    :min="5"
                    :max="300"
                    :step="5"
                    class="w-full accent-blue-600"
                  />
                  <div class="mt-2 flex justify-between text-sm text-slate-400">
                    <span>5만원</span>

                    <span>300만원</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <p class="mb-3 text-base font-semibold text-slate-400">[수령액 간편 계산기]</p>
              <p class="text-4xl font-extrabold text-blue-600">{{ totalAmount }}만원</p>
              <div class="mt-3 flex items-center gap-2 text-base text-slate-500">
                <span>원금 {{ principal }}만원</span>
                <span class="text-slate-300">|</span>
                <span
                  >예상 이자 세후
                  <span class="font-semibold text-blue-500"
                    >+ {{ afterTaxInterest }}만원</span
                  ></span
                >
              </div>
              <p class="mt-2 text-sm text-slate-400">
                · 예상 수령액은 평균 금리(연 4.0%)를 기준으로 계산된 참고용 금액입니다.
              </p>
            </div>
          </div>

          <!-- 다음 버튼 -->
          <div class="flex justify-end">
            <button
              @click="onNext"
              class="rounded-2xl bg-slate-900 px-8 py-4 text-base font-semibold text-white transition hover:bg-slate-700"
            >
              다음 단계로 →
            </button>
          </div>
        </template>

        <!-- Step 2 콘텐츠 -->
        <template v-else>
          <div class="flex flex-col gap-4">
            <!-- Q1: 나이 -->
            <div
              class="flex items-start justify-between gap-4 rounded-2xl border border-slate-200 bg-white/70 px-6 py-4"
            >
              <div>
                <p class="text-base font-semibold text-slate-800">
                  1. 현재 나이가 어떻게 되시나요 ?
                </p>
                <p class="mt-1 text-sm text-slate-400">
                  청년 우대 상품이나 연령 제한 상품을 확인할 수 있어요.
                </p>
              </div>
              <input
                v-model="birthDate"
                type="date"
                class="shrink-0 rounded-xl border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <!-- Q2~Q5: Y/N 질문 -->
            <div
              v-for="q in ynQuestions"
              :key="q.key"
              class="flex items-center justify-between gap-4 rounded-2xl border border-slate-200 bg-white/70 px-6 py-4"
            >
              <div class="flex-1">
                <p class="text-base font-semibold text-slate-800">{{ q.label }}</p>
                <p class="mt-1 text-sm text-slate-400">{{ q.desc }}</p>
              </div>
              <div class="flex shrink-0 gap-2">
                <button
                  @click="ynAnswers[q.key] = true"
                  class="w-10 rounded-xl py-2 text-base font-bold transition"
                  :class="
                    ynAnswers[q.key] === true
                      ? 'bg-blue-600 text-white'
                      : 'border border-slate-200 bg-white text-slate-500 hover:border-slate-400'
                  "
                >
                  Y
                </button>
                <button
                  @click="ynAnswers[q.key] = false"
                  class="w-10 rounded-xl py-2 text-base font-bold transition"
                  :class="
                    ynAnswers[q.key] === false
                      ? 'bg-blue-600 text-white'
                      : 'border border-slate-200 bg-white text-slate-500 hover:border-slate-400'
                  "
                >
                  N
                </button>
              </div>
            </div>
          </div>

          <!-- 추천받기 버튼 -->
          <div>
            <button
              @click="onNext"
              :disabled="isLoading"
              class="w-full rounded-2xl bg-slate-900 py-4 text-base font-semibold text-white transition hover:bg-slate-700 disabled:opacity-60"
            >
              {{ isLoading ? '저장 중...' : '나에게 맞는 적금 상품 추천받기' }}
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import api from '@/api/index'
import hiWish from '@/assets/img/wishes/hiWish.png'
import questionWish from '@/assets/img/wishes/questionWish.png'

const router = useRouter()
const step = ref(1)
const selectedPeriod = ref(12)
const monthlyAmount = ref(50)
const isLoading = ref(false)
const birthDate = ref('')
const goalStore = useGoalStore()

const periodOptions = [
  { value: 3, label: '3개월' },
  { value: 6, label: '6개월' },
  { value: 12, label: '12개월' },
  { value: 24, label: '24개월' },
  { value: 36, label: '36개월' },
]

const ynQuestions = [
  {
    key: 'salary',
    label: '2. 월급이나 연금을 이 은행 계좌로 받을 수 있나요 ?',
    desc: '급여이체 우대조건이 있는 상품을 추천할 때 활용해요.',
  },
  {
    key: 'auto',
    label: '3. 매달 자동이체로 적금을 납입할 수 있나요 ?',
    desc: '가장 흔한 우대조건 중 하나에요.',
  },
  {
    key: 'card',
    label: '4. 이 은행 카드로 매달 10만원 이상 쓸 수 있나요 ?',
    desc: '카드 실적 우대금리 적용 여부를 확인해요.',
  },
  {
    key: 'housing',
    label: '5. 주택청약종합저축 통장을 가지고 있나요 ?',
    desc: '청약 보유 고객에게 우대금리를 제공하는 상품이 있어요.',
  },
]

const ynAnswers = reactive<Record<string, boolean | null>>({
  salary: null,
  auto: null,
  card: null,
  housing: null,
})

const principal = computed(() => monthlyAmount.value * selectedPeriod.value)
const afterTaxInterest = computed(() => {
  const interest =
    ((monthlyAmount.value * selectedPeriod.value * (selectedPeriod.value + 1)) / 2) * (0.04 / 12)
  return Math.round(interest * (1 - 0.154))
})
const totalAmount = computed(() => principal.value + afterTaxInterest.value)

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
