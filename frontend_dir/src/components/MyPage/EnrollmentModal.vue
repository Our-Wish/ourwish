<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/30"
      @click.self="emit('close')"
    >
      <div class="w-full max-w-md rounded-2xl bg-white p-7 shadow-xl">
        <h2 class="text-xl font-bold text-slate-900">가입 정보 등록</h2>
        <p class="mt-2 text-sm text-slate-400">
          나의 적금 정보를 등록하고 목표 달성 현황을 간편하게 관리해보세요 :)
        </p>

        <div class="mt-6 space-y-4">
          <div>
            <label class="text-sm font-medium text-slate-700">시작 날짜</label>
            <input
              v-model="form.start_date"
              type="date"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base text-slate-800 outline-none focus:border-blue-400"
            />
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700">만기일</label>
            <input
              v-model="form.maturity_date"
              type="date"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base text-slate-800 outline-none focus:border-blue-400"
            />
          </div>

          <div v-if="productType === 'SAVINGS'">
            <label class="text-sm font-medium text-slate-700">월 납입 금액 (만원)</label>
            <input
              v-model.number="form.monthly_amount"
              type="number"
              min="0"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base text-slate-800 outline-none focus:border-blue-400"
            />
          </div>

          <div v-if="productType === 'DEPOSIT'">
            <label class="text-sm font-medium text-slate-700">예치 금액 (만원)</label>
            <input
              v-model.number="form.deposit_amount"
              type="number"
              min="0"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base text-slate-800 outline-none focus:border-blue-400"
            />
          </div>

          <div>
            <label class="text-sm font-medium text-slate-700">금리 (%)</label>
            <input
              v-model.number="form.rate"
              type="number"
              min="0"
              step="0.01"
              class="mt-1 w-full rounded-xl border border-slate-200 px-4 py-2.5 text-base text-slate-800 outline-none focus:border-blue-400"
            />
          </div>
        </div>

        <div class="mt-6 flex gap-2">
          <button
            @click="emit('close')"
            class="flex-1 cursor-pointer rounded-xl border border-slate-200 py-2.5 text-base font-medium text-slate-600 hover:bg-slate-50"
          >
            취소
          </button>
          <button
            @click="submit"
            :disabled="isLoading"
            class="flex-1 cursor-pointer rounded-xl bg-blue-500 py-2.5 text-base font-semibold text-white hover:bg-blue-600 disabled:opacity-50"
          >
            {{ isLoading ? '저장 중...' : '저장' }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import api from '@/api/index'
import type { Enrollment } from '@/stores/enrollment'

const props = defineProps<{
  enrollmentId: number
  productName: string
  productType: 'DEPOSIT' | 'SAVINGS'
  initialData: {
    monthly_amount: number
    deposit_amount?: number
    rate: number
    start_date: string
    maturity_date: string
  }
}>()

const emit = defineEmits<{
  close: []
  updated: [data: Enrollment]
}>()

const isLoading = ref(false)

const form = reactive({
  monthly_amount: props.initialData.monthly_amount ?? 0,
  deposit_amount: props.initialData.deposit_amount ?? 0,
  rate: props.initialData.rate ?? 0,
  start_date: props.initialData.start_date ?? '',
  maturity_date: props.initialData.maturity_date ?? '',
})

async function submit() {
  isLoading.value = true
  try {
    const payload = {
      // 상품군에 맞는 금액만 보낸다. 반대쪽은 null로(백엔드도 반대쪽을 null로 비운다).
      monthly_amount: props.productType === 'SAVINGS' ? form.monthly_amount : null,
      deposit_amount: props.productType === 'DEPOSIT' ? form.deposit_amount : null,
      rate: form.rate,
      start_date: form.start_date,
      maturity_date: form.maturity_date,
    }

    const { data } = await api.patch(`/api/v1/enrollments/${props.enrollmentId}/`, payload)
    emit('updated', data)
    emit('close')
  } catch {
    alert('저장에 실패했어요. 다시 시도해주세요.')
  } finally {
    isLoading.value = false
  }
}
</script>
