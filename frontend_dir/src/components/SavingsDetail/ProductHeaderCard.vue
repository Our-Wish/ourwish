<template>
  <div class="mb-6 overflow-hidden rounded-3xl bg-white shadow-[0_4px_24px_rgba(15,23,42,0.08)]">
    <div class="flex w-full items-stretch px-8 py-7">
      <div class="flex w-1/2 items-center gap-5">
        <div
          class="flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl text-2xl font-extrabold text-white"
          :style="{
            background: `linear-gradient(145deg, ${product.bankColor}cc, ${product.bankColor})`,
            boxShadow: `0 4px 12px ${product.bankColor}38`,
          }"
        >
          {{ product.bankName[0] }}
        </div>
        <div class="min-w-0">
          <p class="text-sm font-medium text-[#64748B]">{{ product.bankName }}</p>
          <p class="mt-1 text-3xl font-extrabold tracking-tight text-[#0F172A]">
            {{ product.productName }}
          </p>
          <div class="mt-3 flex flex-wrap gap-1.5">
            <span
              v-for="tag in product.tags"
              :key="tag"
              class="rounded-full border border-blue-100 bg-blue-50 px-2.5 py-0.5 text-xs font-medium text-blue-600 transition-colors hover:bg-blue-100"
              >#{{ tag }}</span
            >
            <span
              v-if="!product.tags.length"
              class="rounded-full bg-slate-50 px-2.5 py-0.5 text-xs font-medium text-slate-400"
              >기본금리형</span
            >
          </div>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="mx-6 w-px shrink-0 self-stretch bg-slate-100"></div>

      <!-- 중앙: 금리 -->
      <div class="flex w-2/5 flex-col justify-center">
        <p class="text-sm font-semibold uppercase tracking-widest text-[#64748B]">최고 금리</p>
        <p class="mt-2 text-4xl font-black leading-none tracking-tight text-[#2563EB]">
          연 {{ product.maxRate }}<span class="text-[1.75rem]">%</span>
        </p>
        <p class="mt-3 text-sm text-[#64748B]">
          기본금리 {{ product.baseRate }}%<span
            v-if="bonusRate > 0"
            class="ml-1.5 font-semibold text-indigo-500"
          >
            + 우대금리 {{ bonusRate.toFixed(1) }}%p
          </span>
        </p>
      </div>

      <!-- 구분선 -->
      <div class="mx-6 w-px shrink-0 self-stretch bg-slate-100"></div>

      <!-- 우: 액션 버튼 -->
      <div class="flex w-1/5 flex-col justify-center gap-2.5">
        <a
          :href="bankUrl"
          target="_blank"
          class="flex items-center justify-center rounded-xl bg-[#2563EB] py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-700"
        >
          자세히 알아보기 →
        </a>
        <button
          @click="$emit('toggle-favorite')"
          class="flex items-center justify-center gap-1.5 rounded-xl border py-2.5 text-sm font-semibold transition"
          :class="
            isFavorite
              ? 'border-blue-300 bg-blue-50 text-blue-600'
              : 'border-slate-200 text-slate-600 hover:border-slate-300'
          "
        >
          {{ isFavorite ? '♥' : '♡' }} 상품 찜하기
        </button>
        <button
          @click="$emit('select-product')"
          class="flex items-center justify-center rounded-xl border border-slate-200 py-2.5 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:text-slate-900"
        >
          상품 등록하기
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { ProductDetail } from '@/types/product'

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
</script>
