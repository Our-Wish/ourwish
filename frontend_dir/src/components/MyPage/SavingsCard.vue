<template>
  <div class="rounded-2xl border border-slate-200 bg-white p-5">
    <div class="flex items-start justify-between">
      <div class="flex items-center gap-3">
        <div
          class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full text-sm font-bold text-white"
          :style="{ backgroundColor: bankColor }"
        >
          {{ bankInitial }}
        </div>
        <div>
          <p class="text-xs text-slate-400">{{ bankName }}</p>
          <p class="text-base font-bold text-slate-900">{{ trimProductName(productName) }}</p>
        </div>
      </div>
      <span class="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-500">
        D- {{ dDay }}
      </span>
    </div>

    <div class="mt-4 flex items-center justify-between">
      <p class="text-sm text-slate-500">{{ currentAmount }}만원 / 만기 {{ maturityAmount }}만원</p>
      <p class="text-sm font-bold text-blue-500">{{ progress }}%</p>
    </div>
    <div class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
      <div class="h-full rounded-full bg-blue-500 transition-all" :style="{ width: `${progress}%` }" />
    </div>

    <div class="mt-4 flex items-center justify-between">
      <p class="text-sm text-slate-500">
        다음 납입 <span class="font-semibold text-slate-800">{{ nextPaymentDate }}</span>
      </p>
      <p class="text-sm font-semibold text-slate-800">월 {{ monthlyAmount }}만원</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { trimProductName } from '@/utils/product'

defineProps<{
  bankInitial: string
  bankColor: string
  bankName: string
  productName: string
  dDay: number
  currentAmount: number
  maturityAmount: number
  progress: number
  nextPaymentDate: string
  monthlyAmount: number
}>()
</script>
