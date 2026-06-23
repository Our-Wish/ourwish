<template>
  <div class="relative rounded-2xl bg-white p-5 ring-1 ring-slate-200">
    <button
      @click="emit('delete', id)"
      class="absolute right-4 top-4 flex h-6 w-6 cursor-pointer items-center justify-center text-xs text-slate-400 hover:bg-slate-50"
    >
      ✕
    </button>

    <div class="flex items-start gap-3 pr-8">
      <div
        class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-base font-bold text-white"
        :style="{ backgroundColor: bankColor }"
      >
        {{ bankName[0] }}
      </div>

      <template v-if="isFilled">
        <div class="flex-1">
          <p class="text-xs text-slate-400">{{ bankName }}</p>
          <div class="flex items-center gap-4">
            <button
              @click="router.push({ name: 'savings-detail', params: { id: productId } })"
              class="cursor-pointer text-lg pt-0.5 font-bold text-slate-900 hover:text-blue-700"
            >
              {{ trimProductName(productName) }}
            </button>
            <div class="h-2 flex-1 overflow-hidden rounded-full bg-slate-100">
              <div
                class="h-full rounded-full bg-blue-400 transition-all"
                :style="{ width: `${progress}%` }"
              />
            </div>
          </div>
          <p class="mt-1 text-sm text-slate-400">
            시작 날짜 : {{ startDate }} | 월 납입 금액 : {{ monthlyAmount }}만원 | 금리 :
            {{ rate }}% | 만기일 : {{ maturityDate }}
          </p>
        </div>
        <div class="shrink-0 text-right">
          <p class="text-sm font-semibold text-red-400">{{ progress }}% 달성했어요 !</p>
          <button
            @click="showModal = true"
            class="mt-1 cursor-pointer text-sm text-slate-400 hover:text-slate-600"
          >
            정보 수정하기 →
          </button>
        </div>
      </template>

      <template v-else>
        <div class="flex-1">
          <p class="text-xs text-slate-400">{{ bankName }}</p>
          <button
            @click="router.push({ name: 'savings-detail', params: { id: productId } })"
            class="cursor-pointer text-lg font-bold text-slate-900 hover:text-blue-700"
          >
            {{ trimProductName(productName) }}
          </button>
          <p class="mt-1 text-sm text-slate-400">
            목표 금액과 기간을 입력해 달성률을 확인해보세요.
          </p>
        </div>
        <button
          @click="showModal = true"
          class="shrink-0 self-end cursor-pointer text-sm text-slate-400 hover:text-slate-600"
        >
          정보 입력하기
        </button>
      </template>
    </div>

    <EnrollmentModal
      v-if="showModal"
      :enrollment-id="id"
      :product-name="productName"
      :product-type="productType"
      :initial-data="{ monthly_amount: monthlyAmount, rate, start_date: startDate, maturity_date: maturityDate }"
      @close="showModal = false"
      @updated="onUpdated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { trimProductName } from '@/utils/product'
import { useRouter } from 'vue-router'
import type { EnrolledProductCardProps } from '@/types/product'
import EnrollmentModal from '@/components/MyPage/EnrollmentModal.vue'

const router = useRouter()

defineProps<EnrolledProductCardProps>()

const emit = defineEmits<{
  delete: [id: number]
  updated: [data: any]
}>()

const showModal = ref(false)

function onUpdated(data: any) {
  emit('updated', data)
}
</script>
