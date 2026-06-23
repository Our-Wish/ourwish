<template>
  <div class="relative">
    <div
      v-if="deletingId !== null"
      class="absolute right-0 top-0 z-20 w-72 rounded-2xl bg-white p-5 shadow-xl ring-1 ring-slate-100"
    >
      <p class="text-base font-bold text-slate-900">정말 상품을 삭제하시겠습니까 ?</p>
      <p class="mt-1 text-sm text-slate-400">지금 상품을 삭제하면 기록이 완전히 삭제됩니다</p>
      <div class="mt-4 flex gap-2">
        <button
          @click="confirmDelete"
          class="flex-1 cursor-pointer rounded-xl border border-slate-200 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50"
        >
          삭제
        </button>
        <button
          @click="deletingId = null"
          class="flex-1 cursor-pointer rounded-xl bg-blue-500 py-2 text-sm font-semibold text-white hover:bg-blue-600"
        >
          유지하기
        </button>
      </div>
    </div>

    <h1 class="text-4xl font-extrabold text-slate-900">찜한 상품 관리</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      내가 관심있어하는 예·적금 상품을 한눈에 관리해보세요.
    </p>

    <div class="mt-8 flex overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <button
        @click="activeTab = 'deposit'"
        class="flex-1 cursor-pointer py-4 text-base font-semibold transition"
        :class="
          activeTab === 'deposit' ? 'bg-blue-50 text-blue-600' : 'text-slate-400 hover:bg-slate-50'
        "
      >
        예금 관리
      </button>
      <button
        @click="activeTab = 'savings'"
        class="flex-1 cursor-pointer py-4 text-base font-semibold transition"
        :class="
          activeTab === 'savings'
            ? 'bg-blue-50 text-blue-600 ring-1 ring-blue-200'
            : 'text-slate-400 hover:bg-slate-50'
        "
      >
        적금 관리
      </button>
    </div>

    <div class="mt-6 space-y-4">
      <div
        v-for="product in displayProducts"
        :key="product.id"
        class="relative rounded-2xl bg-white p-5 ring-1 ring-slate-200"
      >
        <button
          @click="deletingId = product.id"
          class="absolute right-4 top-4 flex h-6 w-6 cursor-pointer items-center justify-center text-xs text-slate-400 hover:bg-slate-50"
        >
          ✕
        </button>

        <div class="flex items-start gap-3 pr-8">
          <div
            class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full text-base font-bold text-white"
            :style="{ backgroundColor: product.bankColor }"
          >
            {{ product.bankName[0] }}
          </div>
          <div class="flex-1">
            <p class="text-xs text-slate-400">{{ product.bankName }}</p>
            <button
              @click="router.push({ name: 'savings-detail', params: { id: product.id } })"
              class="cursor-pointer text-lg pt-0.5 font-bold text-slate-900 hover:text-blue-700"
            >
              {{ product.productName }}
            </button>
            <p class="text-lg font-bold text-slate-900"></p>
            <p class="mt-1 text-sm text-slate-400">
              기본 금리 {{ product.baseRate }}% | 최고 금리 {{ product.maxRate }}%
            </p>
          </div>
        </div>
      </div>

      <div v-if="displayProducts.length === 0" class="py-20 text-center text-base text-slate-300">
        찜한 상품이 없어요.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFavoritesStore } from '@/stores/favorites'
import { bankColorMap } from '@/constants/bankColors'
import { trimProductName } from '@/utils/product'

const router = useRouter()

const favoritesStore = useFavoritesStore()
const activeTab = ref<'deposit' | 'savings'>('deposit')
const deletingId = ref<number | null>(null)

const displayProducts = computed(() => {
  const filtered = favoritesStore.favorites.filter((item) =>
    activeTab.value === 'deposit'
      ? item.product_type === 'DEPOSIT'
      : item.product_type === 'SAVINGS',
  )
  return filtered.map((item) => ({
    id: item.product_id,
    bankName: item.bank_name,
    bankColor: bankColorMap[item.bank_name] ?? '#6366f1',
    productName: trimProductName(item.product_name),
    bankType: item.bank_type,
    baseRate: item.base_rate,
    maxRate: item.max_rate,
    expectedPayout: item.expected_payout,
  }))
})

onMounted(() => favoritesStore.fetchFavorites())

async function confirmDelete() {
  if (deletingId.value === null) return
  try {
    await favoritesStore.removeFavorite(deletingId.value)
  } catch {
    alert('찜 해제에 실패했어요.')
  } finally {
    deletingId.value = null
  }
}
</script>
