<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div class="flex px-32 pb-12 pt-8">
      <aside class="w-1/4 mt-12 pr-8">
        <img :src="happyWish" alt="위시" class="mx-auto w-44" />
        <p class="mt-6 text-center text-base font-bold text-slate-700">
          {{ authStore.user?.nickname ?? '사용자' }} 님 조건에 맞는 상품을 골라봤어요 !
        </p>

        <div class="mt-4 rounded-2xl bg-slate-50 p-4 ring-1 ring-slate-200">
          <p class="text-xs font-semibold text-slate-400">예치 플랜</p>
          <div class="mt-2 space-y-1.5">
            <div class="flex justify-between">
              <span class="text-sm text-slate-500">예치 기간</span>
              <span class="text-sm font-bold text-slate-800"
                >{{ goalStore.depositPeriod }}개월</span
              >
            </div>
            <div class="flex justify-between">
              <span class="text-sm text-slate-500">예치 금액</span>
              <span class="text-sm font-bold text-slate-800"
                >{{ goalStore.depositAmount }}만원</span
              >
            </div>
          </div>

          <div class="mt-3 border-t border-slate-200 pt-3">
            <p class="text-xs font-semibold text-slate-400">우대금리 조건</p>
            <div class="mt-2 flex flex-wrap gap-1.5">
              <span
                v-for="chip in conditionChips"
                :key="chip"
                class="rounded-lg bg-white px-3 py-1 text-xs text-slate-600 ring-1 ring-slate-200"
              >
                {{ chip }}
              </span>
            </div>
          </div>
        </div>

        <p class="mt-6 text-center text-xs font-thin text-slate-40 break-keep">
          추천 결과는 참고용으로 제공되며, 실제 적용 금리와 우대조건은 가입 시점의 상품 정보와
          개인별 조건에 따라 달라질 수 있어요.
        </p>
      </aside>

      <div class="w-px bg-slate-200" />

      <main class="flex-1 px-14 pt-2">
        <div class="flex items-start justify-between">
          <div>
            <h1 class="text-4xl font-extrabold text-slate-900">추천 상품 목록</h1>
            <p class="mt-3 text-base font-light text-slate-400">
              예상 세후 수령액은 달라질 수 있으며, 수령액이 높은 순으로 정렬됩니다.

              <br />
              우대금리순 선택 시, 선택한 우대조건을 모두 충족하는 상품의 예상 수령액 기준으로
              정렬됩니다.
            </p>
          </div>

          <div class="flex flex-col items-end gap-2 mt-1">
            <div class="relative">
              <button
                @click="showSortDropdown = !showSortDropdown"
                class="flex items-center gap-2 rounded-xl border border-slate-200 bg-white px-5 py-2.5 text-base font-medium text-slate-700 transition hover:border-slate-300"
              >
                {{ currentSortLabel }}
                <span class="text-slate-400">▼</span>
              </button>

              <div
                v-if="showSortDropdown"
                class="fixed inset-0 z-10"
                @click="showSortDropdown = false"
              />
              <div
                v-if="showSortDropdown"
                class="absolute right-0 top-full z-20 mt-2 w-64 overflow-hidden rounded-2xl bg-white shadow-xl ring-1 ring-slate-100"
              >
                <button
                  v-for="opt in sortOptions"
                  :key="opt.apiSort"
                  @click="selectSort(opt)"
                  class="w-full px-5 py-3.5 text-left text-base font-medium transition"
                  :class="
                    currentSort === opt.apiSort
                      ? 'bg-indigo-500 text-white'
                      : 'text-slate-700 hover:bg-slate-50'
                  "
                >
                  {{ opt.label }}
                </button>
              </div>
            </div>

            <BankFilterDropdown v-model="selectedBanks" />
          </div>
        </div>

        <div v-if="isLoading" class="mt-16 text-center text-base text-slate-400">
          불러오는 중...
        </div>

        <div v-else>
          <div class="mt-6 grid grid-cols-2 gap-4">
            <ProductCard
              v-for="product in visibleProducts"
              :key="product.id"
              :id="product.id"
              :bank-name="product.bankName"
              :bank-color="product.bankColor"
              :product-name="product.productName"
              :product-type="product.productType"
              :amount="product.amount"
              :max-rate="product.maxRate"
              :base-rate="product.baseRate"
              :condition="product.condition"
            />
          </div>

          <div v-if="visibleCount < filteredProducts.length" class="mt-10 text-center">
            <button
              @click="visibleCount += 6"
              class="rounded-full px-12 py-3.5 text-base font-medium text-slate-500 transition hover:text-slate-800 cursor-pointer"
            >
              더 보기
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import api from '@/api/index'
import { useGoalStore } from '@/stores/goal'
import { useAuthStore } from '@/stores/auth'
import ProductCard from '@/components/Recommendation/ProductCard.vue'
import BankFilterDropdown from '@/components/Recommendation/BankFilterDropdown.vue'
import { bankColorMap } from '@/constants/bankColors'
import { FIRST_TIER_BANKS } from '@/constants/banks'
import { TAG_LABELS as CONDITION_LABELS } from '@/constants/tagLabels'
import happyWish from '@/assets/img/wishes/happyWish.png'

const goalStore = useGoalStore()
const authStore = useAuthStore()
const rawProducts = ref<any[]>([])
const isLoading = ref(false)
const showSortDropdown = ref(false)
const selectedBanks = ref<string[]>([])
const visibleCount = ref(6)
const conditionChips = ref<string[]>([])

watch(selectedBanks, () => {
  visibleCount.value = 6
})

type ApiSort = 'base' | 'max' | 'all'

interface SortOption {
  apiSort: ApiSort
  label: string
  shortLabel: string
}

const sortOptions: SortOption[] = [
  { apiSort: 'max', label: '최고 금리 수령액순', shortLabel: '최고 금리 순' },
  { apiSort: 'base', label: '기본 금리 수령액순', shortLabel: '기본 금리 순' },
  { apiSort: 'all', label: '내 조건 기준 수령액순', shortLabel: '우대 금리 순' },
]

const currentSort = ref<ApiSort>('max')

const currentSortLabel = computed(
  () => sortOptions.find((o) => o.apiSort === currentSort.value)?.shortLabel ?? '기본 금리 순',
)

function selectSort(opt: SortOption) {
  currentSort.value = opt.apiSort
  showSortDropdown.value = false
  fetchProducts()
}

const products = computed(() =>
  rawProducts.value.map((item: any) => ({
    id: item.product_id,
    bankName: item.bank_name,
    bankColor: bankColorMap[item.bank_name] ?? '#6366f1',
    productName: item.product_name,
    productType: '예금',
    baseRate: item.base_rate,
    maxRate: item.max_rate,
    amount: Math.round(item.expected_payout / 10000),
    condition: item.matched_tags ?? [],
  })),
)

const filteredProducts = computed(() => {
  if (selectedBanks.value.length === 0) return products.value
  return products.value.filter((p) =>
    selectedBanks.value.some((key) => {
      if (key === 'first_tier') return FIRST_TIER_BANKS.has(p.bankName)
      if (key === 'savings') return p.bankName.includes('저축은행')
      return p.bankName === key
    }),
  )
})

const visibleProducts = computed(() => filteredProducts.value.slice(0, visibleCount.value))

const fetchProfile = async () => {
  try {
    const { data } = await api.get('/api/v1/search-profile/')
    const chips: string[] = []
    if (data.birth_date) chips.push(CONDITION_LABELS['birth_date']!)
    if (data.first_transaction) chips.push(CONDITION_LABELS['first_transaction']!)
    if (data.online_signup) chips.push(CONDITION_LABELS['online_signup']!)
    if (data.marketing_consent) chips.push(CONDITION_LABELS['marketing_consent']!)
    if (data.redeposit) chips.push(CONDITION_LABELS['redeposit']!)
    conditionChips.value = chips
  } catch {}
}

const fetchProducts = async () => {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/v1/products/recommend/', {
      params: {
        sort: currentSort.value,
        product_type: 'DEPOSIT',
      },
    })
    rawProducts.value = data.results
  } catch {
    alert('상품 목록을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchProfile()
  fetchProducts()
})
</script>
