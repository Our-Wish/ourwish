<template>
  <div>
    <h1 class="text-4xl font-extrabold text-slate-900">가입 상품 금리 비교</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      가입한 상품의 금리를 한눈에 비교해보세요.<br />
      기본·최고·내 가입금리를 한국은행 평균 금리(점선)와 함께 확인할 수 있어요.
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
  type Plugin,
} from 'chart.js'
import api from '@/api/index'
import { useEnrollmentStore } from '@/stores/enrollment'
import { useMarketRatesStore } from '@/stores/marketRates'
import { trimProductName } from '@/utils/product'

Chart.register(BarController, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

interface RateItem {
  label: string
  baseRate: number
  maxRate: number
  myRate: number
  productType: 'DEPOSIT' | 'SAVINGS'
}

const enrollmentStore = useEnrollmentStore()
const marketRates = useMarketRatesStore()
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
  await enrollmentStore.fetchEnrollments()

  const results = await Promise.all(
    enrollmentStore.enrollments.map(async (e) => {
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

  // 현재 탭에 맞는 한국은행 평균(연 %) — 예금 탭=정기예금, 적금 탭=정기적금
  const avgRate = activeTab.value === 'deposit' ? marketRates.depositAvg : marketRates.savingsAvg
  // ECOS 실패(폴백) 땐 '한국은행'이라 하면 거짓이므로 '시중 평균'으로 표기
  const avgSource = marketRates.isFallback ? '시중 평균' : '한국은행 평균'
  const avgAsOf =
    !marketRates.isFallback && marketRates.asOf ? ` (${marketRates.asOf.replace('-', '.')})` : ''
  const avgLabel = `${avgSource}${avgAsOf} ${avgRate}%`

  const allRates = filteredItems.value.flatMap((i) => [i.baseRate, i.maxRate, i.myRate])
  const yMax = Math.max(...allRates, avgRate) + 2

  // 막대 위에 한국은행 평균 금리 가로 점선 + 라벨을 직접 그린다.
  // (line 데이터셋은 상품이 1개면 선이 안 그려져, 플러그인으로 항상 보이게 한다)
  const avgLinePlugin: Plugin<'bar'> = {
    id: 'avgRateLine',
    afterDatasetsDraw(chart) {
      const yScale = chart.scales.y
      if (!yScale) return
      const y = yScale.getPixelForValue(avgRate)
      const { left, right } = chart.chartArea
      const ctx = chart.ctx
      ctx.save()
      ctx.beginPath()
      ctx.setLineDash([5, 5])
      ctx.lineWidth = 1.5
      ctx.strokeStyle = 'rgba(245, 158, 11, 0.8)'
      ctx.moveTo(left, y)
      ctx.lineTo(right, y)
      ctx.stroke()
      ctx.setLineDash([])

      ctx.font = '600 11px sans-serif'
      ctx.textAlign = 'right'
      ctx.textBaseline = 'bottom'
      ctx.fillStyle = 'rgba(180, 110, 0, 1)'
      ctx.fillText(avgLabel, right - 6, y - 4)
      ctx.restore()
    },
  }

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
    plugins: [avgLinePlugin],
  })
}

async function switchTab(tab: 'deposit' | 'savings') {
  activeTab.value = tab
  await nextTick()
  buildChart()
}

onMounted(async () => {
  // 평균 금리도 받아와야 기준선을 그릴 수 있으므로 함께 기다린다.
  await Promise.all([loadData(), marketRates.fetchMarketRates()])
  buildChart()
})

onUnmounted(() => {
  chartInstance?.destroy()
})
</script>
