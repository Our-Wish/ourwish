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

    <h1 class="text-4xl font-extrabold text-slate-900">나의 상품 관리</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      가입한 예·적금 상품을 한눈에 관리해보세요.
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
      <EnrolledProductCard
        v-for="product in displayProducts"
        :key="product.id"
        v-bind="product"
        @delete="deletingId = $event"
        @updated="savingsStore.updateEnrollment($event)"
      />

      <div v-if="displayProducts.length === 0" class="py-20 text-center text-base text-slate-300">
        등록된 상품이 없어요.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useSavingsStore } from '@/stores/savings'
import { bankColorMap } from '@/constants/bankColors'
import EnrolledProductCard from '@/components/MyPage/EnrolledProductCard.vue'

const savingsStore = useSavingsStore()
const activeTab = ref<'deposit' | 'savings'>('deposit')
const deletingId = ref<number | null>(null)

const displayProducts = computed(() => {
  const filtered = savingsStore.enrollments.filter((item) =>
    activeTab.value === 'deposit'
      ? item.product_type === 'DEPOSIT'
      : item.product_type === 'SAVINGS',
  )
  return filtered.map((item) => ({
    id: item.enrollment_id,
    productId: item.product_id,
    productType: item.product_type,
    bankName: item.bank_name,
    bankColor: bankColorMap[item.bank_name] ?? '#6366f1',
    productName: item.product_name,
    isFilled: item.is_filled,
    monthlyAmount: item.monthly_amount,
    depositAmount: item.deposit_amount,
    rate: item.rate,
    startDate: item.start_date,
    maturityDate: item.maturity_date,
    progress: item.achievement_gauge,
  }))
})

onMounted(() => savingsStore.fetchEnrollments())

function confirmDelete() {
  if (deletingId.value === null) return
  savingsStore.removeEnrollment(deletingId.value)
  deletingId.value = null
}
</script>
