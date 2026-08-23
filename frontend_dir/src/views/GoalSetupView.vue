<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-8">
    <div class="flex flex-col px-5 pb-12 lg:flex-row lg:px-32 lg:pb-0">
      <div class="flex flex-col justify-between lg:w-1/3 lg:pl-8">
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
          <h1 class="mt-3 text-3xl font-extrabold leading-tight text-slate-900 md:text-5xl">
            <template v-if="step === 1">{{ config.step1Title[0] }}<br />{{ config.step1Title[1] }}</template>
            <template v-else>{{ config.step2Title[0] }}<br />{{ config.step2Title[1] }}</template>
          </h1>
          <p class="mt-4 text-base leading-relaxed text-slate-500 md:mt-5 md:text-lg">
            <template v-if="step === 1">
              {{ config.step1Desc[0] }}<br />{{ config.step1Desc[1] }}
            </template>
            <template v-else>
              {{ config.step2Desc[0] }}<br />{{ config.step2Desc[1] }}
            </template>
          </p>
        </div>
        <img :src="step === 1 ? hiWish : fightingWish" class="mt-10 hidden w-60 self-start lg:block" />
      </div>
      <div class="hidden w-px bg-slate-200 lg:block" />

      <div class="flex flex-1 flex-col justify-between pt-8 lg:px-16 lg:pt-10">
        <template v-if="step === 1">
          <div class="flex flex-col gap-8">
            <div>
              <p class="mb-4 text-lg font-medium text-slate-700">{{ config.periodLabel }}</p>
              <div class="grid grid-cols-3 gap-2 md:flex md:gap-3">
                <button
                  v-for="option in periodOptions"
                  :key="option.value"
                  @click="selectedPeriod = option.value"
                  class="flex-1 rounded-2xl border-2 py-3 text-sm font-semibold transition md:text-base"
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
              <p class="mb-4 text-lg font-medium text-slate-700">{{ config.amountLabel }}</p>
              <div class="rounded-2xl border border-slate-200 bg-white/70 px-6 py-5">
                <div class="flex items-center gap-2">
                  <input
                    v-model.number="amount"
                    type="text"
                    inputmode="numeric"
                    :class="isSavings ? 'w-20' : 'w-28'"
                    class="rounded-xl border border-slate-200 bg-white px-3 py-1.5 text-2xl font-extrabold text-slate-900 outline-none focus:border-blue-400 focus:ring-2 focus:ring-blue-100"
                  />
                  <span class="text-2xl font-extrabold text-slate-900">만원</span>
                </div>
                <div class="mt-4">
                  <input
                    v-model.number="amount"
                    type="range"
                    :min="5"
                    :max="config.amountMax"
                    :step="5"
                    class="w-full accent-blue-600"
                  />
                  <div class="mt-2 flex justify-between text-sm text-slate-400">
                    <span>5만원</span>
                    <span>{{ config.amountMax }}만원</span>
                  </div>
                </div>
              </div>
            </div>

            <div>
              <p class="mb-3 text-base font-semibold text-slate-600">{{ config.calcTitle }}</p>
              <p class="text-3xl font-extrabold text-blue-600 md:text-4xl">{{ formatWon(totalAmount) }}</p>
              <div class="mt-3 flex flex-wrap items-center gap-2 text-sm text-slate-500 md:text-base">
                <span>원금 {{ formatWon(isSavings ? principal : amount) }}</span>
                <span class="text-slate-300">|</span>
                <span
                  >예상 이자 세후
                  <span class="font-semibold text-blue-500">+ {{ formatWon(afterTaxInterest) }}</span>
                </span>
              </div>
              <p class="mt-2 text-sm text-slate-400">
                * 예상 수령액은 {{ rateCaption }}를 기준으로 한 참고용 금액이에요.<br />실제
                수령액은 상품·우대조건에 따라 달라질 수 있어요.
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
                    나이에 따라 가입 가능한 상품을 확인할 때 활용해요.
                  </p>
                </div>
                <input
                  v-model="birthDate"
                  type="date"
                  class="shrink-0 w-36 rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-500 placeholder:text-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div
                v-for="q in config.ynQuestions"
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
              {{ isLoading ? '저장 중...' : config.submitText }}
            </button>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import { useMarketRatesStore } from '@/stores/marketRates'
import { useAuthStore } from '@/stores/auth'
import api from '@/api/index'
import { formatWon } from '@/utils/format'
import hiWish from '@/assets/img/wishes/hiWish.png'
import fightingWish from '@/assets/img/wishes/fightingWish.png'

const props = defineProps<{ type: 'savings' | 'deposit' }>()
const isSavings = computed(() => props.type === 'savings')

const router = useRouter()
const goalStore = useGoalStore()
const marketRates = useMarketRatesStore()
const authStore = useAuthStore()

const step = ref(1)
const selectedPeriod = ref(12)
const amount = ref(50)
const isLoading = ref(false)
const birthDate = ref('')
const savedProfile = ref<Record<string, unknown>>({})

const periodOptions = [
  { value: 3, label: '3개월' },
  { value: 6, label: '6개월' },
  { value: 12, label: '12개월' },
  { value: 24, label: '24개월' },
  { value: 36, label: '36개월' },
]

const savingsQuestions = [
  { key: 'salary', label: '2. 월급이나 연금을 이 은행 계좌로 받을 수 있나요 ?', desc: '급여이체 우대조건이 있는 상품을 추천할 때 활용해요.' },
  { key: 'auto', label: '3. 매달 자동이체로 적금을 납입할 수 있나요 ?', desc: '자동이체 우대조건을 확인할 때 활용해요.' },
  { key: 'card', label: '4. 이 은행 카드로 매달 10만원 이상 쓸 수 있나요 ?', desc: '카드 사용 실적 우대금리 적용 여부를 확인할 때 활용해요.' },
  { key: 'housing', label: '5. 주택청약종합저축 통장을 가지고 있나요 ?', desc: '청약통장 보유 우대금리 적용 여부를 확인할 때 활용해요.' },
]

const depositQuestions = [
  { key: 'first_transaction', label: '2. 해당 은행과 첫 거래이신가요?', desc: '첫 거래 고객 우대금리 적용 여부를 확인할 때 활용해요.' },
  { key: 'online_signup', label: '3. 비대면으로 가입하실 수 있나요?', desc: '비대면 가입 우대조건을 확인할 때 활용해요.' },
  { key: 'marketing_consent', label: '4. 마케팅 정보 수신에 동의하실 수 있나요?', desc: '마케팅 동의 우대금리 적용 여부를 확인할 때 활용해요.' },
  { key: 'redeposit', label: '5. 만기 후 재예치하실 계획이 있으신가요?', desc: '재예치 우대조건을 확인할 때 활용해요.' },
]

const config = computed(() =>
  isSavings.value
    ? {
        step1Title: ['얼마나 모을지', '먼저 정해볼게요'],
        step2Title: ['더 높은 금리를', '받을 수 있어요'],
        step1Desc: ['저축 기간과 매달 넣을 금액을 알려주시면', '목표에 맞는 적금 후보를 찾아드릴게요.'],
        step2Desc: ['실제로 받을 수 있는 금리는 사람마다 달라요.', '조건이 맞을수록 더 높은 금리를 받을 수 있어요.'],
        periodLabel: '1. 저축 기간',
        amountLabel: '2. 월 저축 금액',
        amountMax: 300,
        calcTitle: '[수령액 간편 계산기]',
        submitText: '나에게 맞는 적금 상품 추천받기',
        ynQuestions: savingsQuestions,
      }
    : {
        step1Title: ['얼마를 맡길지', '먼저 정해볼게요'],
        step2Title: ['더 좋은 금리를', '찾아볼게요'],
        step1Desc: ['예치 기간과 예치 금액을 알려주시면', '조건에 맞는 예금 상품을 찾아드릴게요.'],
        step2Desc: ['예금 상품마다 우대조건이 달라요.', '회원님이 받을 수 있는 최대 금리를 찾아드릴게요.'],
        periodLabel: '1. 예치 기간',
        amountLabel: '2. 예치 금액',
        amountMax: 5000,
        calcTitle: '[만기 수령액 예상]',
        submitText: '나에게 맞는 예금 상품 추천받기',
        ynQuestions: depositQuestions,
      },
)

const ynAnswers = reactive<Record<string, boolean | null>>({
  salary: null, auto: null, card: null, housing: null,
  first_transaction: null, online_signup: null, marketing_consent: null, redeposit: null,
})

onMounted(() => marketRates.fetchMarketRates())

const fetchSearchProfile = async () => {
  try {
    const { data } = await api.get('/api/v1/search-profile/')
    savedProfile.value = data
    if (data.save_term) selectedPeriod.value = data.save_term
    if (data.birth_date) birthDate.value = data.birth_date
    if (isSavings.value) {
      if (data.monthly_amount) amount.value = data.monthly_amount / 10000
      if (data.salary_transfer !== undefined) ynAnswers.salary = data.salary_transfer
      if (data.auto_transfer !== undefined) ynAnswers.auto = data.auto_transfer
      if (data.card_usage !== undefined) ynAnswers.card = data.card_usage
      if (data.housing_subscription !== undefined) ynAnswers.housing = data.housing_subscription
    } else {
      if (data.deposit_amount) amount.value = data.deposit_amount / 10000
      if (data.first_transaction !== undefined) ynAnswers.first_transaction = data.first_transaction
      if (data.online_signup !== undefined) ynAnswers.online_signup = data.online_signup
      if (data.marketing_consent !== undefined) ynAnswers.marketing_consent = data.marketing_consent
      if (data.redeposit !== undefined) ynAnswers.redeposit = data.redeposit
    }
  } catch {}
}

// 비로그인: 이 탭에서 이전에 입력했던 값(sessionStorage)으로 prefill
const prefillFromStore = () => {
  if (goalStore.birthDate) birthDate.value = goalStore.birthDate
  if (isSavings.value) {
    selectedPeriod.value = goalStore.savings.period
    amount.value = goalStore.savings.monthlyAmount
    const a = goalStore.savings.answers
    if (a) {
      ynAnswers.salary = a.salary_transfer
      ynAnswers.auto = a.auto_transfer
      ynAnswers.card = a.card_usage
      ynAnswers.housing = a.housing_subscription
    }
  } else {
    selectedPeriod.value = goalStore.deposit.period
    amount.value = goalStore.deposit.amount
    const a = goalStore.deposit.answers
    if (a) Object.assign(ynAnswers, a)
  }
}

watch(
  () => authStore.isAuthenticated,
  (isAuth) => (isAuth ? fetchSearchProfile() : prefillFromStore()),
  { immediate: true },
)

const rateAvg = computed(() => isSavings.value ? marketRates.savingsAvg : marketRates.depositAvg)
const principal = computed(() => amount.value * selectedPeriod.value)

const afterTaxInterest = computed(() => {
  const annualRate = rateAvg.value / 100
  const interest = isSavings.value
    ? ((amount.value * selectedPeriod.value * (selectedPeriod.value + 1)) / 2) * (annualRate / 12)
    : amount.value * annualRate * (selectedPeriod.value / 12)
  return Math.round(interest * (1 - 0.154))
})

const totalAmount = computed(() => (isSavings.value ? principal.value : amount.value) + afterTaxInterest.value)

const rateCaption = computed(() => {
  const label = isSavings.value ? '정기적금' : '정기예금'
  return marketRates.isFallback
    ? `시중 평균 금리(연 ${rateAvg.value}%)`
    : `한국은행 ${label} 평균 금리(연 ${rateAvg.value}%, ${marketRates.asOf?.replace('-', '.')} 기준)`
})

const onNext = async () => {
  if (step.value === 1) {
    step.value++
    window.scrollTo(0, 0)
  } else {
    const unanswered = config.value.ynQuestions.some((q) => ynAnswers[q.key] === null)
    if (!birthDate.value || unanswered) {
      alert('모든 항목에 답변해주세요.')
      return
    }
    // 비로그인: 서버 프로필 대신 브라우저(sessionStorage)에 조건을 두고 추천으로 이동
    if (!authStore.isAuthenticated) {
      goalStore.setBirthDate(birthDate.value)
      if (isSavings.value) {
        goalStore.setSavingsGoal(selectedPeriod.value, amount.value, {
          salary_transfer: ynAnswers.salary === true,
          auto_transfer: ynAnswers.auto === true,
          card_usage: ynAnswers.card === true,
          housing_subscription: ynAnswers.housing === true,
        })
        router.push({ name: 'recommendation' })
      } else {
        goalStore.setDepositGoal(selectedPeriod.value, amount.value, {
          first_transaction: ynAnswers.first_transaction === true,
          online_signup: ynAnswers.online_signup === true,
          marketing_consent: ynAnswers.marketing_consent === true,
          redeposit: ynAnswers.redeposit === true,
        })
        router.push({ name: 'depositrecommendation' })
      }
      return
    }

    isLoading.value = true
    try {
      if (isSavings.value) {
        await api.put('/api/v1/search-profile/', {
          save_term: selectedPeriod.value,
          monthly_amount: amount.value * 10000,
          birth_date: birthDate.value,
          salary_transfer: ynAnswers.salary,
          auto_transfer: ynAnswers.auto,
          card_usage: ynAnswers.card,
          housing_subscription: ynAnswers.housing,
        })
        goalStore.setSavingsGoal(selectedPeriod.value, amount.value)
        router.push({ name: 'recommendation' })
      } else {
        await api.put('/api/v1/search-profile/', {
          monthly_amount: savedProfile.value.monthly_amount ?? 500000,
          salary_transfer: savedProfile.value.salary_transfer ?? false,
          auto_transfer: savedProfile.value.auto_transfer ?? false,
          card_usage: savedProfile.value.card_usage ?? false,
          housing_subscription: savedProfile.value.housing_subscription ?? false,
          ...savedProfile.value,
          save_term: selectedPeriod.value,
          deposit_amount: amount.value * 10000,
          birth_date: birthDate.value,
          first_transaction: ynAnswers.first_transaction,
          online_signup: ynAnswers.online_signup,
          marketing_consent: ynAnswers.marketing_consent,
          redeposit: ynAnswers.redeposit,
        })
        goalStore.setDepositGoal(selectedPeriod.value, amount.value)
        router.push({ name: 'depositrecommendation' })
      }
    } catch {
      alert('목표 저장에 실패했어요. 다시 시도해주세요.')
    } finally {
      isLoading.value = false
    }
  }
}
</script>
