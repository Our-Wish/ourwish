<template>
  <div>
    <h1 class="text-4xl font-extrabold text-slate-900">가입 상품 금리 비교</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      가입한 상품의 금리를 한눈에 비교해보세요.<br />
      기본금리와 최고금리, 실제 적용 금리를 확인할 수 있어요.
    </p>

    <div class="mt-8 flex overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <button
        @click="switchTab('deposit')"
        class="flex-1 cursor-pointer py-4 text-base font-semibold transition"
        :class="
          activeTab === 'deposit' ? 'bg-blue-50 text-blue-600' : 'text-slate-400 hover:bg-slate-50'
        "
      >
        예금
      </button>
      <button
        @click="switchTab('savings')"
        class="flex-1 cursor-pointer py-4 text-base font-semibold transition"
        :class="
          activeTab === 'savings'
            ? 'bg-blue-50 text-blue-600 ring-1 ring-blue-200'
            : 'text-slate-400 hover:bg-slate-50'
        "
      >
        적금
      </button>
    </div>

    <div v-if="isLoading" class="py-20 text-center text-base text-slate-400">불러오는 중...</div>

    <div v-else-if="filteredItems.length === 0" class="py-20 text-center text-base text-slate-300">
      등록된 상품이 없어요.
    </div>

    <div v-else class="mt-6 rounded-2xl bg-white p-8 shadow-sm ring-1 ring-slate-100">
      <canvas ref="chartCanvas" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import {
  Chart,
  BarController,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js'
import api from '@/api/index'
import { useSavingsStore } from '@/stores/savings'
import { trimProductName } from '@/utils/product'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

interface RateItem {
  label: string
  baseRate: number
  maxRate: number
  myRate: number
  productType: 'DEPOSIT' | 'SAVINGS'
}

const savingsStore = useSavingsStore()
const chartCanvas = ref<HTMLCanvasElement | null>(null)
const isLoading = ref(true)
const activeTab = ref<'deposit' | 'savings'>('deposit')
const items = ref<RateItem[]>([])
let chartInstance: Chart | null = null

const filteredItems = computed(() =>
  items.value.filter((i) =>
    activeTab.value === 'deposit' ? i.productType === 'DEPOSIT' : i.productType === 'SAVINGS',
  ),
)

async function loadData() {
  await savingsStore.fetchEnrollments()

  const results = await Promise.all(
    savingsStore.enrollments.map(async (e) => {
      try {
        const { data } = await api.get(`/api/v1/products/${e.product_id}/`)
        const option = data.options?.[0] ?? {}
        return {
          label: `${e.bank_name} · ${trimProductName(e.product_name)}`,
          baseRate: +(option.base_rate ?? data.base_rate ?? 0),
          maxRate: +(option.max_rate ?? data.max_rate ?? 0),
          myRate: +e.rate,
          productType: e.product_type,
        } as RateItem
      } catch {
        return null
      }
    }),
  )

  items.value = results.filter((r): r is RateItem => r !== null)
  isLoading.value = false
}

function buildChart() {
  if (!chartCanvas.value || filteredItems.value.length === 0) return

  const allRates = filteredItems.value.flatMap((i) => [i.baseRate, i.maxRate, i.myRate])
  const yMax = Math.max(...allRates) + 2

  if (chartInstance) {
    chartInstance.destroy()
    chartInstance = null
  }

  chartInstance = new Chart(chartCanvas.value, {
    type: 'bar',
    data: {
      labels: filteredItems.value.map((i) => i.label),
      datasets: [
        {
          label: '기본금리',
          data: filteredItems.value.map((i) => i.baseRate),
          backgroundColor: 'rgba(148, 163, 184, 0.45)',
          borderRadius: 2,
          barPercentage: 0.7,
          categoryPercentage: 0.6,
        },
        {
          label: '최고금리',
          data: filteredItems.value.map((i) => i.maxRate),
          backgroundColor: 'rgba(129, 140, 248, 0.65)',
          borderRadius: 2,
          barPercentage: 0.7,
          categoryPercentage: 0.6,
        },
        {
          label: '내 가입금리',
          data: filteredItems.value.map((i) => i.myRate),
          backgroundColor: 'rgba(37, 99, 235, 0.85)',
          borderRadius: 2,
          barPercentage: 0.7,
          categoryPercentage: 0.6,
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          labels: { font: { size: 12 } },
        },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ${ctx.parsed.y}%`,
          },
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          max: yMax,
          ticks: {
            callback: (val) => `${val}%`,
            font: { size: 13 },
          },
          title: {
            display: true,
            text: '금리 (%)',
            font: { size: 14 },
          },
        },
        x: {
          ticks: { font: { size: 12 } },
        },
      },
    },
  })
}

async function switchTab(tab: 'deposit' | 'savings') {
  activeTab.value = tab
  await nextTick()
  buildChart()
}

onMounted(async () => {
  await loadData()
  buildChart()
})

onUnmounted(() => {
  chartInstance?.destroy()
})
</script>
