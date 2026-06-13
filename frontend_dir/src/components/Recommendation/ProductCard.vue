<template>
  <div class="cursor-pointer rounded-2xl border border-slate-200 bg-white p-5 transition hover:shadow-md" @click="router.push({ name: 'savings-detail', params: { id: props.id } })">
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-3">
        <span class="text-sm font-bold text-slate-400">{{ rank }}</span>
        <div
          class="flex h-9 w-9 items-center justify-center rounded-full text-sm font-bold text-white"
          :style="{ backgroundColor: bankColor }"
        >
          {{ bankName[0] }}
        </div>
        <div>
          <p class="text-xs text-slate-400">{{ bankName }} · 적금</p>
          <p class="font-bold text-slate-900">{{ productName }}</p>
        </div>
      </div>
      <span class="rounded-full px-3 py-1 text-xs font-medium" :class="difficultyClass">
        {{ difficulty }}
      </span>
    </div>

    <div class="mt-4 flex items-end justify-between">
      <div>
        <p class="text-xs text-slate-400">세후 수령액</p>
        <p class="text-xl font-extrabold text-slate-900">{{ amount }}만원</p>
      </div>
      <div class="text-right">
        <p class="text-xs text-slate-400">최고금리</p>
        <p class="text-lg font-bold text-blue-600">연 {{ maxRate }}%</p>
        <p class="text-xs text-slate-400">기본 {{ baseRate }}%</p>
      </div>
    </div>

    <div class="mt-3 rounded-xl bg-slate-50 px-4 py-2 text-sm text-slate-600">
      우대조건 {{ condition }}
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
  difficulty: '쉬움' | '보통' | '어려움'
  amount: number
  maxRate: number
  baseRate: number
  condition: string
}>()

const difficultyMap: Record<'쉬움' | '보통' | '어려움', string> = {
  쉬움: 'bg-green-100 text-green-700',
  보통: 'bg-yellow-100 text-yellow-700',
  어려움: 'bg-red-100 text-red-700',
}

const difficultyClass = computed(() => difficultyMap[props.difficulty])
</script>
