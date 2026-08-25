<template>
  <div
    class="mb-6 overflow-hidden rounded-3xl border border-blue-100 bg-gradient-to-r from-white via-white to-blue-50 shadow-[0_12px_40px_rgba(37,99,235,0.12)]"
  >
    <div class="flex w-full flex-col items-stretch gap-6 px-5 py-6 lg:flex-row lg:gap-0 lg:px-9 lg:py-8">
      <div class="flex items-center gap-4 lg:w-1/2 lg:gap-6">
        <div
          class="flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl text-2xl font-black text-white shadow-lg md:h-20 md:w-20 md:rounded-3xl md:text-3xl"
          :style="{
            background: `linear-gradient(145deg, ${product.bankColor}dd, ${product.bankColor})`,
            boxShadow: `0 10px 24px ${product.bankColor}38`,
          }"
        >
          {{ product.bankName[0] }}
        </div>

        <div class="min-w-0">
          <div class="mb-2 flex items-center gap-2">
            <span class="text-sm font-medium text-[#64748B]">
              {{ product.bankName }}
            </span>
          </div>

          <p class="text-2xl font-black tracking-tight text-[#0F172A] md:text-4xl">
            {{ product.productName }}
          </p>

          <div class="mt-4 flex flex-wrap gap-1.5">
            <span
              v-for="tag in product.tags"
              :key="tag"
              class="rounded-full border border-blue-100 bg-white px-3 py-1 text-xs font-semibold text-blue-600"
            >
              #{{ tag }}
            </span>

            <span
              v-if="!product.tags.length"
              class="rounded-full bg-slate-50 px-3 py-1 text-xs font-semibold text-slate-400"
            >
              기본금리형
            </span>
          </div>
        </div>
      </div>

      <div class="mx-7 hidden w-px shrink-0 self-stretch bg-blue-100 lg:block"></div>

      <div class="flex flex-col justify-center lg:w-2/5">
        <div class="flex items-center justify-between">
          <p class="text-sm font-bold tracking-widest text-[#64748B]">최고 금리</p>
          <button
            @click="showCalc = true"
            class="rounded-full bg-slate-100 px-3.5 py-1.5 text-sm font-semibold text-slate-500 transition hover:bg-blue-50 hover:text-blue-500"
          >
            예상 수령액 계산기
          </button>
        </div>

        <p class="mt-2 text-5xl font-black leading-none tracking-tight text-[#2563EB] md:text-6xl">
          {{ product.maxRate }}<span class="text-3xl">%</span>
        </p>

        <div class="mt-4 inline-flex w-fit items-center rounded-xl bg-white px-4 py-2 shadow-xs">
          <p class="text-sm font-semibold text-[#64748B]">
            기본 {{ product.baseRate }}%
            <span v-if="bonusRate > 0" class="ml-1 text-blue-600">
              + 우대 {{ bonusRate.toFixed(1) }}%p
            </span>
          </p>
        </div>
      </div>

      <div class="mx-7 hidden w-px shrink-0 self-stretch bg-blue-100 lg:block"></div>

      <div class="flex flex-col justify-center gap-2.5 lg:w-1/5">
        <a
          :href="bankUrl"
          target="_blank"
          class="flex items-center justify-center rounded-2xl bg-[#2563EB] py-3 text-sm font-bold text-white shadow-lg shadow-blue-200 transition hover:bg-blue-700 active:scale-95"
        >
          자세히 알아보기 →
        </a>

        <button
          @click="$emit('toggle-favorite')"
          class="flex items-center justify-center gap-1.5 rounded-2xl border py-3 text-sm font-bold transition active:scale-95"
          :class="
            isFavorite
              ? 'border-blue-300 bg-blue-50 text-blue-600'
              : 'border-slate-200 bg-white text-slate-600 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600'
          "
        >
          상품 찜하기 {{ isFavorite ? '♥' : '♡' }}
        </button>

        <button
          @click="$emit('select-product')"
          class="flex items-center justify-center rounded-2xl border border-slate-200 bg-white py-3 text-sm font-bold text-slate-700 transition hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600 active:scale-95"
        >
          상품 등록하기
        </button>
      </div>
    </div>
  </div>

  <DepositCalcModal
    v-if="showCalc && product.productType === 'deposit'"
    :base-rate="product.baseRate"
    :max-rate="product.maxRate"
    :bonus-rate="bonusRate"
    :intr-rate-type="intrRateType"
    @close="showCalc = false"
  />
  <SavingsCalcModal
    v-if="showCalc && product.productType === 'savings'"
    :base-rate="product.baseRate"
    :max-rate="product.maxRate"
    :bonus-rate="bonusRate"
    :intr-rate-type="intrRateType"
    @close="showCalc = false"
  />
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { ProductDetail } from '@/types/product'
import type { IntrRateType } from '@/utils/payout'
import DepositCalcModal from './DepositCalcModal.vue'
import SavingsCalcModal from './SavingsCalcModal.vue'

const props = defineProps<{
  product: Pick<
    ProductDetail,
    | 'bankName'
    | 'bankColor'
    | 'productName'
    | 'baseRate'
    | 'maxRate'
    | 'tags'
    | 'productType'
    | 'intr_rate_type'
  >
  isFavorite: boolean
  bonusRate: number
  bankUrl: string
}>()

// 계산기가 단리/복리를 구분하도록 넘긴다. 'M'이 아니면 단리로 본다.
const intrRateType = computed<IntrRateType>(() =>
  props.product.intr_rate_type === 'M' ? 'M' : 'S',
)

defineEmits<{
  'toggle-favorite': []
  'select-product': []
}>()

const showCalc = ref(false)
</script>
