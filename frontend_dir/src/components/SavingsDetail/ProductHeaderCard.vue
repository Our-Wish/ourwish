<template>
  <div
    class="mb-6 overflow-hidden rounded-3xl border border-blue-100 bg-gradient-to-r from-white via-white to-blue-50 shadow-[0_12px_40px_rgba(37,99,235,0.12)]"
  >
    <div class="flex w-full items-stretch px-9 py-8">
      <div class="flex w-1/2 items-center gap-6">
        <div
          class="flex h-20 w-20 shrink-0 items-center justify-center rounded-3xl text-3xl font-black text-white shadow-lg"
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

          <p class="text-4xl font-black tracking-tight text-[#0F172A]">
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

      <div class="mx-7 w-px shrink-0 self-stretch bg-blue-100"></div>

      <div class="flex w-2/5 flex-col justify-center">
        <div class="flex items-center justify-between">
          <p class="text-sm font-bold tracking-widest text-[#64748B]">최고 금리</p>
          <button
            @click="showCalc = true"
            class="rounded-full bg-slate-100 px-3.5 py-1.5 text-sm font-semibold text-slate-500 transition hover:bg-blue-50 hover:text-blue-500"
          >
            예상 수령액 계산기
          </button>
        </div>

        <p class="mt-2 text-6xl font-black leading-none tracking-tight text-[#2563EB]">
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

      <div class="mx-7 w-px shrink-0 self-stretch bg-blue-100"></div>

      <div class="flex w-1/5 flex-col justify-center gap-2.5">
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

  <CalcModal
    v-if="showCalc"
    :base-rate="product.baseRate"
    :max-rate="product.maxRate"
    :bonus-rate="bonusRate"
    @close="showCalc = false"
  />
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { ProductDetail } from '@/types/product'
import CalcModal from './CalcModal.vue'

defineProps<{
  product: Pick<
    ProductDetail,
    'bankName' | 'bankColor' | 'productName' | 'baseRate' | 'maxRate' | 'tags'
  >
  isFavorite: boolean
  bonusRate: number
  bankUrl: string
}>()

defineEmits<{
  'toggle-favorite': []
  'select-product': []
}>()

const showCalc = ref(false)
</script>
