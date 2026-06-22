<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-8">
    <div class="flex px-32">
      <div class="flex w-1/3 flex-col pl-8 justify-between">
        <button
          @click="step--"
          :class="step === 1 ? 'invisible' : ''"
          class="cursor-pointer self-start text-sm mb-2 text-slate-400 transition hover:text-slate-700"
        >
          ← 이전 단계로
        </button>
        <div>
          <p class="text-xl font-semibold text-blue-600">
            {{ step === 1 ? 'STEP 01' : 'STEP 02' }}
          </p>

          <h1 class="mt-3 text-5xl font-extrabold leading-tight text-slate-900">
            <template v-if="step === 1">얼마를 맡길지<br />먼저 정해볼게요</template>
            <template v-else>더 좋은 금리를 <br />찾아볼게요</template>
          </h1>
          <p class="mt-5 text-lg leading-relaxed text-slate-500">
            <template v-if="step === 1">
              예치 기간과 예치 금액을 알려주시면<br />조건에 맞는 예금 상품을 찾아드릴게요.
            </template>
            <template v-else>
              예금 상품마다 우대조건이 달라요.<br />회원님이 받을 수 있는 최대 금리를 찾아드릴게요.
            </template>
          </p>
        </div>
        <img :src="step === 1 ? hiWish : fightingWish" class="mt-10 w-60 self-start" />
      </div>
      <div class="w-px bg-slate-200" />

      <div class="flex flex-1 flex-col justify-between px-16 pt-10">
        <template v-if="step === 1">
          <div class="flex flex-col gap-8">
            <div>
              <p class="mb-4 text-lg font-medium text-slate-700">1. 예치 기간</p>
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
              <p class="mb-4 text-lg font-medium text-slate-700">2. 예치 금액</p>
              <div class="rounded-2xl border border-slate-200 bg-white/70 px-6 py-5">
                <div class="flex items-center justify-between">
                  <p class="text-2xl font-extrabold text-slate-900">{{ depositAmount }}만원</p>
                </div>
                <div class="mt-4">
                  <input
                    v-model.number="depositAmount"
                    type="range"
                    :min="5"
                    :max="5000"
                    :step="10"
                    class="w-full accent-blue-600"
                  />
                  <div class="mt-2 flex justify-between text-sm text-slate-400">
                    <span>5만원</span>

                    <span>5000만원</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <p class="mb-3 text-base font-semibold text-slate-600">[만기 수령액 예상]</p>
              <p class="text-4xl font-extrabold text-blue-600">{{ totalAmount }}만원</p>
              <div class="mt-3 flex items-center gap-2 text-base text-slate-500">
                <span>예치금 {{ depositAmount }}만원</span>
                <span class="text-slate-300">|</span>
                <span
                  >예상 이자 세후
                  <span class="font-semibold text-blue-500"
                    >+ {{ afterTaxInterest }}만원</span
                  ></span
                >
              </div>
              <p class="mt-2 text-sm text-slate-400">
                * 예상 수령액은 평균 금리(연 3.5%)를 기준으로 계산한 참고용 금액입니다.<br />실제
                수령액은 상품별 금리와 우대조건에 따라 달라질 수 있습니다.
              </p>
            </div>
          </div>

          <div class="flex justify-end">
            <button
              @click="onNext"
              class="cursor-pointer rounded-2xl mr-2 text-lg font-semibold transition hover:text-slate-400"
            >
              다음 단계로 →
            </button>
          </div>
        </template>

        <template v-else>
          <div class="flex flex-col gap-8">
            <div class="flex flex-col divide-y divide-slate-200">
              <div class="flex items-center justify-between gap-4 py-5">
                <div>
                  <p class="text-base font-semibold text-slate-800">
                    1. 현재 나이가 어떻게 되시나요 ?
                  </p>
                  <p class="mt-1 text-sm text-slate-400">
                    연령 우대 상품 가입 가능 여부를 확인해요.
                  </p>
                </div>
                <input
                  v-model="birthDate"
                  type="date"
                  class="shrink-0 w-36 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-500 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div
                v-for="q in ynQuestions"
                :key="q.key"
                class="flex items-center justify-between gap-4 py-5"
              >
                <div class="flex-1">
                  <p class="text-base font-semibold text-slate-800">{{ q.label }}</p>
                  <p class="mt-1 text-sm text-slate-400">{{ q.desc }}</p>
                </div>
                <div class="flex shrink-0 gap-2">
                  <button
                    @click="ynAnswers[q.key] = true"
                    class="h-11 w-11 rounded-xl text-base font-bold transition"
                    :class="
                      ynAnswers[q.key] === true
                        ? 'bg-blue-600 text-white'
                        : 'border border-slate-200 bg-white text-slate-400 hover:border-slate-400'
                    "
                  >
                    Y
                  </button>
                  <button
                    @click="ynAnswers[q.key] = false"
                    class="h-11 w-11 rounded-xl text-base font-bold transition"
                    :class="
                      ynAnswers[q.key] === false
                        ? 'bg-blue-600 text-white'
                        : 'border border-slate-200 bg-white text-slate-400 hover:border-slate-400'
                    "
                  >
                    N
                  </button>
                </div>
              </div>
            </div>

            <button
              @click="onNext"
              :disabled="isLoading"
              class="w-full rounded-2xl bg-slate-900 py-4 text-base font-semibold text-white transition hover:bg-slate-700 disabled:opacity-60"
            >
              {{ isLoading ? '저장 중...' : '나에게 맞는 예금 상품 추천받기' }}
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
import hiWish from '@/assets/img/wishes/hiWish.png'
import fightingWish from '@/assets/img/wishes/fightingWish.png'

const router = useRouter()
const step = ref(1)
const selectedPeriod = ref(12)
const depositAmount = ref(50)
const isLoading = ref(false)
const birthDate = ref('')

const periodOptions = [
  { value: 3, label: '3개월' },
  { value: 6, label: '6개월' },
  { value: 12, label: '12개월' },
  { value: 24, label: '24개월' },
  { value: 36, label: '36개월' },
]

const ynQuestions = [
  {
    key: 'first_deal',
    label: '2. 해당 은행과 첫 거래이신가요?',
    desc: '첫 거래 고객 우대금리를 확인해요.',
  },
  {
    key: 'non_face',
    label: '3. 비대면으로 가입하실 수 있나요?',
    desc: '비대면 가입 전용 상품을 추천해드려요.',
  },
  {
    key: 'marketing',
    label: '4. 마케팅 정보 수신에 동의하실 수 있나요?',
    desc: '마케팅 동의 우대금리 적용 여부를 확인해요.',
  },
  {
    key: 'renewal',
    label: '5. 만기 후 재예치하실 계획이 있으신가요?',
    desc: '재예치 우대 혜택이 있는 상품을 확인해요.',
  },
]

const ynAnswers = reactive<Record<string, boolean | null>>({
  first_deal: null,
  non_face: null,
  marketing: null,
  renewal: null,
})

const afterTaxInterest = computed(() => {
  const interest = depositAmount.value * 0.035 * (selectedPeriod.value / 12)
  return Math.round(interest * (1 - 0.154))
})
const totalAmount = computed(() => depositAmount.value + afterTaxInterest.value)

const onNext = async () => {
  if (step.value === 1) {
    step.value++
    window.scrollTo(0, 0)
  } else {
    const unanswered = ynQuestions.some((q) => ynAnswers[q.key] === null)
    if (!birthDate.value || unanswered) {
      alert('모든 항목에 답변해주세요.')
      return
    }

    isLoading.value = true
    try {
      // TODO: 예금 전용 API 연동
      router.push({ name: 'depositrecommendation' })
    } catch {
      alert('목표 저장에 실패했어요. 다시 시도해주세요.')
    } finally {
      isLoading.value = false
    }
  }
}
</script>
