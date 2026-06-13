<template>
  <div class="min-h-screen bg-slate-50">
    <header class="flex items-center px-5 py-4">
      <button @click="router.go(-1)" class="flex items-center gap-1 text-sm text-slate-600">
        <span>‹</span>
        <span>뒤로</span>
      </button>
    </header>

    <div v-if="product" class="px-5 pb-12">
      <!-- 상단 카드 -->
      <div class="rounded-3xl p-6 text-white" :style="{ backgroundColor: product.bankColor }">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <div
              class="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 text-sm font-bold"
            >
              {{ product.bankName[0] }}
            </div>
            <span class="text-sm font-medium opacity-90">{{ product.bankName }} · 적금</span>
          </div>
          <span class="rounded-full bg-white/20 px-3 py-1 text-xs font-semibold">★ 우대금리</span>
        </div>

        <h1 class="mt-5 text-2xl font-bold">{{ product.productName }}</h1>

        <div class="my-4 border-t border-white/20" />

        <div class="flex items-end justify-between">
          <div>
            <p class="text-xs opacity-70">현재 예상 금리</p>
            <p class="mt-1 text-4xl font-extrabold">약 {{ product.baseRate.toFixed(2) }}%</p>
          </div>
          <div class="text-right text-sm opacity-90">
            <p class="opacity-70">기본/최고</p>
            <p class="font-semibold">{{ product.baseRate }}% / {{ product.maxRate }}%</p>
          </div>
        </div>

        <a
          :href="product.bankUrl"
          target="_blank"
          class="mt-4 flex w-full items-center justify-between rounded-2xl bg-white/15 px-4 py-3 text-sm font-medium transition hover:bg-white/25"
        >
          <span>{{ product.bankName }}에서 상품 자세히보기</span>
          <span>↗</span>
        </a>
      </div>

      <!-- 핵심 조건 -->
      <div class="mt-8">
        <p class="text-sm font-semibold text-blue-500">핵심 조건</p>
        <p class="mt-1 text-lg font-bold text-slate-900">한눈에 보는 상세 내용</p>

        <div class="mt-4 overflow-hidden rounded-2xl border border-slate-200 bg-white">
          <div
            v-for="(item, index) in product.conditions"
            :key="item.label"
            class="flex items-start gap-6 px-5 py-4"
            :class="{ 'border-t border-slate-100': index > 0 }"
          >
            <span class="w-24 shrink-0 text-sm text-slate-400">{{ item.label }}</span>
            <span class="text-sm font-semibold text-slate-900">{{ item.value }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const productId = computed(() => Number(route.params.id))

type Condition = { label: string; value: string }

type ProductDetail = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  baseRate: number
  maxRate: number
  bankUrl: string
  conditions: Condition[]
}

const DEFAULT_CONDITIONS: Condition[] = [
  { label: '가입 대상', value: '' },
  { label: '가입 방법', value: '' },
  { label: '월 납입 한도', value: '' },
  { label: '만기후 이자율', value: '' },
  { label: '기타 유의사항', value: '' },
]

const mockProductDetails: Record<number, ProductDetail> = {
  1: { id: 1, bankName: '하나은행', bankColor: '#3D8B7A', productName: '청년도약 적금', baseRate: 3.5, maxRate: 5.0, bankUrl: 'https://www.hanabank.com', conditions: DEFAULT_CONDITIONS },
  2: { id: 2, bankName: '신한은행', bankColor: '#0046FF', productName: '신한 첫 월급 적금', baseRate: 3.2, maxRate: 4.5, bankUrl: 'https://www.shinhan.com', conditions: DEFAULT_CONDITIONS },
  3: { id: 3, bankName: '국민은행', bankColor: '#FFCD00', productName: 'KB 청춘적금', baseRate: 3.0, maxRate: 4.0, bankUrl: 'https://www.kbstar.com', conditions: DEFAULT_CONDITIONS },
  4: { id: 4, bankName: '우리은행', bankColor: '#0F6EBF', productName: '우리 첫 거래 적금', baseRate: 3.2, maxRate: 3.8, bankUrl: 'https://www.wooribank.com', conditions: DEFAULT_CONDITIONS },
  5: { id: 5, bankName: '농협은행', bankColor: '#00A650', productName: 'NH 디딤돌 정기적금', baseRate: 3.6, maxRate: 3.6, bankUrl: 'https://www.nonghyup.com', conditions: DEFAULT_CONDITIONS },
}

const product = computed(() => mockProductDetails[productId.value] ?? null)
</script>
