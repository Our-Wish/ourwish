<template>
  <div
    class="group flex cursor-pointer flex-col rounded-2xl border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60"
    @click="router.push({ name: 'savings-detail', params: { id: props.id } })"
  >
    <div class="mb-3 flex flex-wrap gap-2">
      <template v-if="condition.length">
        <span
          v-for="tag in condition"
          :key="tag"
          class="rounded-2xl bg-indigo-50 px-2.5 py-1 text-xs font-light text-indigo-500"
        >
          {{ conditionLabel(tag) }}
        </span>
      </template>
      <span v-else class="rounded-2xl bg-slate-100 px-2.5 py-1 text-xs font-light text-slate-400">
        기본금리형
      </span>
    </div>

    <div class="flex items-start justify-between gap-3">
      <div class="flex items-center gap-3">
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-base font-extrabold text-white"
          :style="{ backgroundColor: bankColor }"
        >
          {{ bankInitial }}
        </div>
        <div>
          <p class="text-sm text-slate-400">{{ bankName }} · 적금</p>
          <p class="mt-1 text-base font-bold text-slate-900">{{ productName }}</p>
        </div>
      </div>
      <div class="shrink-0 text-right">
        <p class="text-xs text-slate-400">최고 금리</p>
        <p class="mt-0.5 text-xl font-extrabold text-indigo-600">연 {{ maxRate }}%</p>
        <p class="text-xs text-slate-400">기본금리 {{ baseRate }}%</p>
      </div>
    </div>

    <div class="mt-auto flex items-end justify-between pt-4">
      <div>
        <p class="text-sm text-slate-400">예상 세후 수령액</p>
        <p class="mt-0.5 text-2xl font-extrabold text-slate-900">{{ formattedAmount }}만원</p>
      </div>
      <span class="text-sm font-semibold text-slate-400 transition group-hover:text-blue-600">
        자세히 보기 →
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps<{
  id: number
  bankName: string
  bankColor: string
  productName: string
  amount: number
  maxRate: number
  baseRate: number
  condition: string[]
}>()

import { TAG_LABELS } from '@/constants/tagLabels'

const conditionLabel = (tag: string) => TAG_LABELS[tag] ?? tag

const bankInitial = computed(() => props.bankName.charAt(0))
const formattedAmount = computed(() => props.amount.toLocaleString())
</script>
