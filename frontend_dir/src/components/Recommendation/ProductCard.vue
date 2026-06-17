<template>
  <div
    class="group cursor-pointer rounded-[24px] border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/70"
    @click="router.push({ name: 'savings-detail', params: { id: props.id } })"
  >
    <!-- 상단: 은행/상품명/난이도 -->
    <div class="flex items-start justify-between gap-4">
      <div class="flex items-center gap-4">
        <span class="w-4 text-base font-bold text-slate-400">{{ rank }}</span>

        <div
          class="flex h-11 w-11 items-center justify-center rounded-full text-base font-extrabold text-white shadow-sm"
          :style="{ backgroundColor: bankColor }"
        >
          {{ bankInitial }}
        </div>

        <div>
          <p class="text-sm font-medium text-slate-400">{{ bankName }} · 적금</p>
          <p class="mt-0.5 text-lg font-extrabold text-slate-900">
            {{ productName }}
          </p>
        </div>
      </div>

      <span class="shrink-0 rounded-full px-3.5 py-1.5 text-sm font-bold" :class="difficultyClass">
        조건 {{ difficulty }}
      </span>
    </div>

    <!-- 중간: 수령액 / 금리 -->
    <div class="mt-4 flex items-end justify-between gap-6">
      <div>
        <p class="text-sm font-medium text-slate-400">예상 세후 수령액</p>
        <p class="mt-0.5 text-2xl font-extrabold tracking-tight text-slate-900">
          {{ formattedAmount }}만원
        </p>
      </div>

      <div class="text-right">
        <p class="text-sm font-medium text-slate-400">최고금리</p>
        <p class="mt-0.5 text-xl font-extrabold text-blue-600">연 {{ maxRate }}%</p>
        <p class="mt-0.5 text-sm font-medium text-slate-400">기본금리 {{ baseRate }}%</p>
      </div>
    </div>

    <!-- 하단: 우대조건 칩 -->
    <div class="mt-4 border-t border-slate-100 pt-3">
      <p class="mb-2 ml-1 text-sm font-semibold text-slate-500">필요 조건</p>

      <div class="flex flex-wrap gap-2">
        <span
          v-for="chip in conditionChips"
          :key="chip"
          class="rounded-full bg-slate-50 px-3 py-1.5 text-sm font-medium text-slate-600 ring-1 ring-slate-100"
        >
          {{ chip }}
        </span>
      </div>
    </div>

    <!-- 클릭 안내 -->
    <div class="flex items-center justify-end text-sm font-semibold text-slate-400">
      <span class="transition group-hover:text-blue-600"> 자세히 보기 → </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps<{
  id: number
  rank: number
  bankName: string
  bankColor: string
  productName: string
  difficulty: '없음' | '쉬움' | '보통' | '어려움'
  amount: number
  maxRate: number
  baseRate: number
  condition: string
}>()

const difficultyMap: Record<'없음' | '쉬움' | '보통' | '어려움', string> = {
  없음: 'bg-slate-100 text-slate-500 ring-1 ring-slate-200',
  쉬움: 'bg-green-50 text-green-700 ring-1 ring-green-100',
  보통: 'bg-yellow-50 text-yellow-700 ring-1 ring-yellow-100',
  어려움: 'bg-red-50 text-red-600 ring-1 ring-red-100',
}

const difficultyClass = computed(() => difficultyMap[props.difficulty])

const bankInitial = computed(() => props.bankName.charAt(0))

const formattedAmount = computed(() => props.amount.toLocaleString())

const conditionChips = computed(() => {
  const raw = props.condition?.trim()

  if (!raw || raw === '없음') {
    return ['우대조건 없음']
  }

  return raw
    .split(/\s*[+·,]\s*/g)
    .map((item) => item.trim())
    .filter(Boolean)
})
</script>
