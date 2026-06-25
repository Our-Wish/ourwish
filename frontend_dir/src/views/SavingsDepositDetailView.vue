<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div v-if="isLoading" class="flex items-center justify-center py-24 text-slate-400">
      불러오는 중...
    </div>

    <div v-else-if="product" class="mx-auto max-w-6xl px-8 pb-16 pt-6">
      <ProductHeaderCard
        :product="product"
        :is-favorite="isFavorite"
        :bonus-rate="bonusRate"
        :bank-url="bankUrl"
        @toggle-favorite="toggleFavorite"
        @select-product="selectProduct"
      />

      <div class="flex items-start gap-5">
        <div class="w-3/5 space-y-4">
          <div class="rounded-[28px] border border-blue-100 bg-white p-7">
            <div class="mb-4 flex items-center gap-3">
              <p class="text-lg font-semibold text-slate-800">✨ AI 상품 요약</p>
            </div>

            <div>
              <ul v-if="product.aiSummaries.length" class="space-y-2.5">
                <li v-for="(s, i) in product.aiSummaries" :key="i" class="flex items-start gap-2.5">
                  <span class="mt-0.5 shrink-0 text-blue-400">•</span>
                  <span class="text-sm leading-7 text-slate-600">{{ s }}</span>
                </li>
              </ul>
              <p v-else class="text-sm leading-7 text-slate-400">AI 요약 정보가 없는 상품이에요.</p>
            </div>
          </div>

          <ProductBasicInfo :conditions="product.conditions" />

          <div class="rounded-2xl bg-white p-6 shadow-sm">
            <p class="text-base font-semibold text-slate-800">우대금리 조건</p>
            <div v-if="product.specialCondition" class="mt-2 ml-1">
              <p class="mt-2 whitespace-pre-line text-sm leading-relaxed break-keep text-slate-600">
                {{ product.specialCondition }}
              </p>
            </div>
            <p v-else class="mt-4 text-sm text-slate-400">우대 조건 정보가 없는 상품이에요</p>
          </div>
        </div>

        <div class="w-2/5 space-y-4">
          <div class="rounded-2xl bg-white p-5 shadow-sm">
            <p class="mb-4 ml-1 text-xl font-semibold text-slate-00">주변 영업점 찾기</p>
            <KakaoMap :bank-name="product.bankName" />
          </div>

          <div class="overflow-hidden rounded-2xl bg-white shadow-sm">
            <div class="flex items-center gap-2.5 bg-blue-300 px-4 py-3">
              <div class="flex h-8 w-8 items-center justify-center rounded-full bg-white/40">
                <img src="@/assets/img/wishes/hiWish.png" class="h-6 w-6 object-contain" />
              </div>
              <div>
                <p class="text-sm font-semibold text-white">OURWISH 챗봇</p>
                <p class="text-xs text-blue-50">금융 상품 AI 도우미, 위시입니다 :)</p>
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
import { TAG_LABELS } from '@/constants/tagLabels'
import type { ProductDetail } from '@/types/product'
import { BANK_URL_MAP } from '@/constants/bankUrls'
import Chat from '@/components/Chat.vue'
import ProductHeaderCard from '@/components/ProductDetail/ProductHeaderCard.vue'
import ProductBasicInfo from '@/components/ProductDetail/ProductBasicInfo.vue'
import KakaoMap from '@/components/ProductDetail/KakaoMap.vue'
import { useEnrollmentStore } from '@/stores/enrollment'
import { useFavoritesStore } from '@/stores/favorites'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const goalStore = useGoalStore()
const enrollmentStore = useEnrollmentStore()
const favoritesStore = useFavoritesStore()
const authStore = useAuthStore()

const productId = computed(() => Number(route.params.id))

const isLoading = ref(false)
const isFavorite = ref(false)

const product = ref<ProductDetail | null>(null)

function cleanText(text: string): string {
  return text
    .split('\n')
    .map((line) => line.replace(/^\s*(\d+\s*[.)]\s*|[*·\-•]\s*)/, '').trim())
    .filter(Boolean)
    .join('\n')
}

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
    productType: data.product_type === 'DEPOSIT' ? 'deposit' : 'savings',
    conditions: [
      { label: '가입 대상', value: data.join_member ? cleanText(data.join_member) : '-' },
      { label: '가입 방법', value: data.join_way ? cleanText(data.join_way) : '-' },
      { label: '월 납입 한도', value: formatLimit(data.max_limit) },
      {
        label: '만기후 이자율',
        value: data.maturity_interest ? cleanText(data.maturity_interest) : '-',
      },
      { label: '기타 유의사항', value: data.etc_note ? cleanText(data.etc_note) : '-' },
    ],
    specialCondition: data.special_condition_raw ? cleanText(data.special_condition_raw) : '',
    aiSummaries: data.ai_summary ? cleanText(data.ai_summary).split('\n').filter(Boolean) : [],
    tags: Object.entries(data.tags ?? {})
      .filter(([, v]) => v)
      .map(([k]) => TAG_LABELS[k] ?? k),
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

const bankUrl = computed(() =>
  product.value ? (BANK_URL_MAP[product.value.bankName as keyof typeof BANK_URL_MAP] ?? '#') : '#',
)

const bonusRate = computed(() => {
  if (!product.value) return 0
  return Math.max(0, product.value.maxRate - product.value.baseRate)
})

async function toggleFavorite() {
  if (!authStore.isAuthenticated) {
    authStore.openLoginModal()
    return
  }
  if (!product.value) return
  try {
    if (isFavorite.value) {
      await api.delete(`/api/v1/favorites/${product.value.id}/`)
      favoritesStore.removeFavorite(product.value.id)
    } else {
      const { data } = await api.post('/api/v1/favorites/', { product_id: product.value.id })
      favoritesStore.addFavorite(data)
    }
    isFavorite.value = !isFavorite.value
    alert(isFavorite.value ? '관심 상품에 추가했어요.' : '관심 상품에서 제거됐어요.')
  } catch {
    alert('찜하기 처리에 실패했어요. 다시 시도해주세요.')
  }
}

async function selectProduct() {
  if (!authStore.isAuthenticated) {
    authStore.openLoginModal()
    return
  }
  if (!product.value) return
  try {
    const { data } = await api.post('/api/v1/enrollments/', { product_id: product.value.id })
    enrollmentStore.addEnrollment(data)
    router.push({ name: 'mypage' })
  } catch (err: any) {
    if (err?.response?.status === 409) {
      alert('이미 등록된 상품이에요.')
      router.push({ name: 'mypage' })
    } else {
      alert('상품 가입에 실패했어요. 다시 시도해주세요.')
    }
  }
}
</script>
