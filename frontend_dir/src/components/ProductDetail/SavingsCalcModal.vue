<template>
  <Teleport to="body">
    <div
      @click.self="$emit('close')"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 px-4 backdrop-blur-sm"
    >
      <div class="w-full max-w-sm rounded-3xl bg-white p-8 shadow-2xl">
        <div class="mb-6 flex items-center justify-between">
          <p class="text-lg font-bold text-slate-800">예상 수령액 계산기</p>
          <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>

        <div class="space-y-4">
          <div>
            <p class="mb-2 text-sm font-semibold text-slate-500">매달 넣을 금액 (만원)</p>
            <input
              v-model.number="calcAmount"
              type="number"
              min="1"
              class="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base focus:border-blue-400 focus:outline-none"
              placeholder="예: 30"
            />
          </div>

          <div>
            <p class="mb-2 text-sm font-semibold text-slate-500">저축 기간</p>
            <div class="flex gap-2">
              <button
                v-for="m in [6, 12, 24, 36]"
                :key="m"
                @click="calcPeriod = m"
                class="flex-1 rounded-xl border py-2 text-sm font-semibold transition"
                :class="
                  calcPeriod === m
                    ? 'border-blue-500 bg-blue-500 text-white'
                    : 'border-slate-200 text-slate-600 hover:border-blue-300'
                "
              >
                {{ m }}개월
              </button>
            </div>
          </div>

          <div>
            <div class="mb-2 flex items-center justify-between">
              <p class="text-sm font-semibold text-slate-500">적용 금리 (%)</p>
              <div class="flex gap-1.5">
                <button
                  @click="calcRate = baseRate"
                  class="rounded-xl px-2 py-0.5 text-xs font-medium transition"
                  :class="
                    calcRate === baseRate
                      ? 'bg-slate-700 text-white'
                      : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                  "
                >
                  기본 금리 {{ baseRate }}%
                </button>
                <button
                  @click="calcRate = maxRate"
                  class="rounded-xl px-2 py-0.5 text-xs font-medium transition"
                  :class="
                    calcRate === maxRate
                      ? 'bg-blue-500 text-white'
                      : 'bg-blue-50 text-blue-500 hover:bg-blue-100'
                  "
                >
                  최고 금리 {{ maxRate }}%
                </button>
              </div>
            </div>
            <input
              v-model.number="calcRate"
              type="number"
              min="0"
              max="30"
              step="0.1"
              class="w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base focus:border-blue-400 focus:outline-none"
            />
          </div>
        </div>

        <div class="my-6 border-t border-slate-100"></div>

        <div class="rounded-2xl bg-blue-50 px-6 py-5">
          <p class="mb-1 text-sm font-semibold text-slate-500">
            예상 수령액 ({{ calcRate }}% 기준)
          </p>
          <p class="text-4xl font-extrabold text-blue-600">
            {{ formatWon(totalAmount) }}
          </p>
          <div class="mt-3 flex items-center gap-2 text-sm text-slate-500">
            <span>원금 {{ formatWon(principal) }}</span>
            <span class="text-slate-300">|</span>
            <span>
              세후 이자
              <span class="font-semibold text-blue-500">+{{ formatWon(afterTaxInterest) }}</span>
            </span>
          </div>
        </div>

        <p class="mt-3 text-xs text-slate-400">* 세금과 단리 기준으로 계산한 예상 금액이에요.</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useGoalStore } from '@/stores/goal'
import { formatWon } from '@/utils/format'

const props = defineProps<{
  baseRate: number
  maxRate: number
  bonusRate: number
}>()

defineEmits<{ close: [] }>()

const goalStore = useGoalStore()

const calcAmount = ref(goalStore.savings.monthlyAmount || 30)
const calcPeriod = ref(goalStore.savings.period || 12)
const calcRate = ref(props.maxRate)

const principal = computed(() => calcAmount.value * calcPeriod.value)
const afterTaxInterest = computed(() => {
  const interest =
    ((calcAmount.value * calcPeriod.value * (calcPeriod.value + 1)) / 2) *
    (calcRate.value / 100 / 12)
  return Math.round(interest * (1 - 0.154))
})
const totalAmount = computed(() => principal.value + afterTaxInterest.value)
</script>
