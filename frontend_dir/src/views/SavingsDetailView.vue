<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div v-if="isLoading" class="flex items-center justify-center py-24 text-slate-400">
      불러오는 중...
    </div>

    <div v-else-if="product" class="mx-auto max-w-6xl px-8 pb-16 pt-6">
      <div
        class="mb-6 overflow-hidden rounded-3xl bg-white shadow-[0_4px_24px_rgba(15,23,42,0.08)]"
      >
        <div class="flex w-full items-stretch px-8 py-7">
          <div class="flex w-2/5 items-center gap-5">
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

          <div class="mx-6 w-px shrink-0 self-stretch bg-slate-100"></div>

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

          <div class="mx-6 w-px shrink-0 self-stretch bg-slate-100"></div>

          <div class="flex w-1/5 flex-col justify-center gap-2.5">
            <a
              :href="product.productUrl || '#'"
              target="_blank"
              class="flex items-center justify-center rounded-xl bg-[#2563EB] py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-700"
            >
              상품 자세히 보기 ->
            </a>
            <button
              @click="isFavorite = !isFavorite"
              class="flex items-center justify-center gap-1.5 rounded-xl border py-2.5 text-sm font-semibold transition"
              :class="
                isFavorite
                  ? 'border-blue-300 bg-blue-50 text-blue-600'
                  : 'border-slate-200 text-slate-600 hover:border-slate-300'
              "
            >
              {{ isFavorite ? '♥' : '♡' }} 관심상품
            </button>
            <button
              @click="selectProduct"
              class="flex items-center justify-center rounded-xl border border-slate-200 py-2.5 text-sm font-semibold text-slate-700 transition hover:border-slate-300 hover:text-slate-900"
            >
              상품 등록하기
            </button>
          </div>
        </div>
      </div>

      <!-- 본문 2칼럼 -->
      <div class="flex items-start gap-5">
        <!-- 왼쪽 (3/5) -->
        <div class="w-3/5 space-y-4">
          <!-- 한눈에 요약 -->
          <div class="rounded-2xl bg-blue-50 p-6">
            <div class="flex items-center gap-2">
              <svg
                class="h-5 w-5 text-blue-500"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path
                  d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"
                />
              </svg>
              <p class="text-base font-bold text-blue-700">한눈에 요약</p>
            </div>
            <ul class="mt-4 space-y-3">
              <li v-for="(s, i) in product.aiSummaries" :key="i" class="flex items-start gap-3">
                <svg
                  class="mt-0.5 h-5 w-5 shrink-0 text-blue-500"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M4.5 12.75l6 6 9-13.5" />
                </svg>
                <span class="text-base text-slate-700">{{ s }}</span>
              </li>
            </ul>
          </div>

          <!-- 상품 기본 정보 -->
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <p class="text-base font-bold text-slate-900">상품 기본 정보</p>
            <div class="mt-3 divide-y divide-slate-100">
              <div
                v-for="item in product.conditions"
                :key="item.label"
                class="flex items-center gap-3 py-2.5"
              >
                <div
                  class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-50"
                >
                  <svg
                    class="h-3.5 w-3.5 text-blue-400"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="1.5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      v-if="item.label === '가입 대상'"
                      d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                    />
                    <path
                      v-else-if="item.label === '가입 방법'"
                      d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 8.25h3m-3 3h3m-6 3h.008v.008H6.75V15z"
                    />
                    <path
                      v-else-if="item.label === '월 납입 한도'"
                      d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"
                    />
                    <path
                      v-else-if="item.label === '만기후 이자율'"
                      d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                    <path
                      v-else
                      d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
                    />
                  </svg>
                </div>
                <span class="w-24 shrink-0 text-sm font-medium text-blue-500">{{
                  item.label
                }}</span>
                <span class="text-sm text-slate-700">{{ item.value }}</span>
              </div>
            </div>
            <p class="mt-4 text-sm text-slate-400">
              ※ 자세한 내용은 상품설명서 및 약관을 확인해주세요.
            </p>
          </div>

          <!-- 우대금리 조건 -->
          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <p class="text-base font-semibold text-slate-800">우대 조건 안내</p>
            <div v-if="product.specialCondition" class="mt-4">
              <p class="mt-2 whitespace-pre-line text-sm leading-relaxed text-slate-600">
                {{ product.specialCondition }}
              </p>
            </div>
            <p v-else class="mt-4 text-sm text-slate-400">우대 조건 정보가 없는 상품이에요</p>
          </div>
        </div>

        <!-- 오른쪽 (2/5): 지도 + 챗봇 -->
        <div class="w-2/5 space-y-4">
          <!-- 근처 영업점 -->
          <div class="rounded-2xl bg-white p-5 shadow-sm">
            <p class="text-base font-bold text-slate-900">근처 영업점 찾기</p>
            <div
              class="mt-4 flex h-44 items-center justify-center rounded-xl bg-slate-100 text-sm text-slate-400"
            >
              지도 영역 (카카오맵)
            </div>
            <div class="mt-4 divide-y divide-slate-100">
              <div v-for="i in 2" :key="i" class="flex items-start gap-3 py-3">
                <div
                  class="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-500 text-xs font-bold text-white"
                >
                  {{ i }}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <p class="text-sm font-medium text-slate-300">- -</p>
                    <span class="rounded bg-slate-100 px-1.5 py-0.5 text-xs text-slate-400"
                      >영업점</span
                    >
                  </div>
                  <p class="mt-0.5 text-sm text-slate-300">위치 정보 없음</p>
                </div>
              </div>
            </div>
            <button
              class="mt-3 w-full rounded-xl border border-slate-200 py-2 text-sm text-slate-400 transition hover:border-slate-300 hover:text-slate-600"
            >
              더 많은 지점 보기 ∨
            </button>
          </div>

          <!-- 챗봇 -->
          <div class="overflow-hidden rounded-2xl bg-white shadow-sm">
            <div class="flex items-center gap-3 bg-blue-500 px-5 py-4">
              <div
                class="flex h-9 w-9 items-center justify-center rounded-full bg-white/20 text-lg"
              >
                🤖
              </div>
              <div>
                <p class="text-base font-semibold text-white">OURWISH 챗봇</p>
                <div class="flex items-center gap-1.5">
                  <div class="h-2 w-2 rounded-full bg-green-400"></div>
                  <p class="text-sm text-blue-100">온라인</p>
                </div>
              </div>
            </div>
            <Chat :productId="product.id" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useGoalStore } from '@/stores/goal'
import api from '@/api/index'
import { bankColorMap } from '@/constants/bankColors'
import Chat from '@/components/Chat.vue'

const router = useRouter()
const route = useRoute()
const goalStore = useGoalStore()

const productId = computed(() => Number(route.params.id))

const isLoading = ref(false)
const isFavorite = ref(false)

type Condition = { label: string; value: string }

const TAG_LABELS: Record<string, string> = {
  salary_transfer: '급여이체',
  auto_transfer: '자동이체',
  card_usage: '카드실적',
  housing_subscription: '주택청약',
}

type ProductDetail = {
  id: number
  bankName: string
  bankColor: string
  productName: string
  baseRate: number
  maxRate: number
  intr_rate_type: string
  rsrv_type: string
  conditions: Condition[]
  specialCondition: string
  aiSummaries: string[]
  tags: string[]
  productUrl: string
}

const product = ref<ProductDetail | null>(null)

function formatLimit(value: number): string {
  if (!value || value > 9e15) return '제한 없음'
  return `${Math.round(value / 10000).toLocaleString()}만원`
}

function buildProduct(data: any): ProductDetail {
  const matchedOption =
    (data.options ?? []).find((o: any) => o.save_term === goalStore.period) ??
    data.options?.[0] ??
    {}

  return {
    id: data.product_id,
    bankName: data.bank_name,
    bankColor: bankColorMap[data.bank_name] ?? '#6366f1',
    productName: data.product_name,
    baseRate: matchedOption.base_rate ?? data.base_rate ?? 0,
    maxRate: matchedOption.max_rate ?? data.max_rate ?? 0,
    intr_rate_type: matchedOption.intr_rate_type ?? 'S',
    rsrv_type: matchedOption.rsrv_type ?? 'S',
    conditions: [
      { label: '가입 대상', value: data.join_member ?? '-' },
      { label: '가입 방법', value: data.join_way ?? '-' },
      { label: '월 납입 한도', value: formatLimit(data.max_limit) },
      { label: '만기후 이자율', value: data.maturity_interest ?? '-' },
      { label: '기타 유의사항', value: data.etc_note ?? '-' },
    ],
    specialCondition: data.special_condition_raw ?? '',
    aiSummaries: data.ai_summary ? data.ai_summary.split('\n').filter(Boolean) : [],
    tags: Object.entries(data.tags ?? {})
      .filter(([, v]) => v)
      .map(([k]) => TAG_LABELS[k] ?? k),
    productUrl: data.product_url ?? '',
  }
}

onMounted(async () => {
  isLoading.value = true
  try {
    const { data } = await api.get(`/api/v1/products/${productId.value}/`)
    product.value = buildProduct(data)
    isFavorite.value = data.is_favorited ?? false
  } catch {
    alert('상품 정보를 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
})

const bonusRate = computed(() => {
  if (!product.value) return 0
  return Math.max(0, product.value.maxRate - product.value.baseRate)
})

async function selectProduct() {
  if (!product.value) return
  try {
    await api.post('/api/v1/enrollments/', {
      product_id: product.value.id,
      monthly_amount: goalStore.monthlyAmount * 10000,
      term_months: goalStore.period,
      intr_rate_type: product.value.intr_rate_type,
      rsrv_type: product.value.rsrv_type,
      transfer_day: 25,
      enrolled_at: new Date().toISOString().split('T')[0],
    })
    router.push({ name: 'mypage' })
  } catch {
    alert('상품 가입에 실패했어요. 다시 시도해주세요.')
  }
}
</script>
