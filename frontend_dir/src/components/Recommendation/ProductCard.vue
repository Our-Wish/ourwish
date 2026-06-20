<template>
  <div
    class="group cursor-pointer rounded-2xl border border-slate-200 bg-white p-5 transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60"
    @click="router.push({ name: 'savings-detail', params: { id: props.id } })"
  >
    <!-- 상단: 은행 로고 + 상품명 / 금리 -->
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
          <p class="mt-0.5 text-base font-bold text-slate-900">{{ productName }}</p>
        </div>
      </div>
      <div class="shrink-0 text-right">
        <p class="text-xs text-slate-400">최고 금리</p>
        <p class="mt-0.5 text-xl font-extrabold text-indigo-600">연 {{ maxRate }}%</p>
        <p class="text-xs text-slate-400">기본금리 {{ baseRate }}%</p>
      </div>
    </div>

    <!-- 하단: 수령액 + 자세히 보기 -->
    <div class="mt-4 flex items-end justify-between">
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

const bankInitial = computed(() => props.bankName.charAt(0))
const formattedAmount = computed(() => props.amount.toLocaleString())
</script>
