<template>
  <div>
    <h2 class="mb-1 text-xl font-bold text-slate-900">금 · 은 시세</h2>
    <p class="mb-6 text-sm text-slate-500">대표적인 안전자산의 가격 흐름을 확인해 보세요.</p>

    <!-- 인사이트 스트립 -->
    <div
      class="mb-6 flex flex-col gap-4 rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-100 sm:flex-row sm:items-center sm:justify-between"
    >
      <p class="text-sm leading-relaxed text-slate-600">
        금·은 시세, 잘 보셨나요?<br class="hidden sm:block" />
        안정적으로 목돈 모으는 <span class="font-semibold text-blue-600">예·적금</span>도 한번
        알아볼까요?
      </p>
      <div class="flex shrink-0 gap-2">
        <RouterLink
          :to="{ name: 'depositgoalsetup' }"
          class="rounded-full bg-blue-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-600 active:scale-95"
        >
          예금 추천
        </RouterLink>
        <RouterLink
          :to="{ name: 'goalsetup' }"
          class="rounded-full bg-blue-500 px-4 py-2.5 text-sm font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-600 active:scale-95"
        >
          적금 추천
        </RouterLink>
      </div>
    </div>

    <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">불러오는 중...</div>

    <template v-else>
      <!-- 컨트롤: 자산 토글 + 기간 선택 -->
      <div
        class="mb-5 flex flex-col gap-4 rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-100 sm:flex-row sm:items-end sm:justify-between"
      >
        <div>
          <span class="mb-1.5 block text-xs font-semibold text-slate-500">자산</span>
          <div class="inline-flex rounded-full bg-slate-100 p-1">
            <button
              v-for="opt in assetOptions"
              :key="opt.value"
              class="rounded-full px-5 py-2 text-sm font-semibold transition"
              :class="
                asset === opt.value
                  ? 'bg-white text-slate-900 shadow-sm'
                  : 'text-slate-500 hover:text-slate-700'
              "
              @click="asset = opt.value"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

        <div class="flex flex-wrap items-end gap-3">
          <label class="block">
            <span class="mb-1.5 block text-xs font-semibold text-slate-500">시작일</span>
            <input
              v-model="startDate"
              type="date"
              :min="dataMinDate"
              :max="endDate || dataMaxDate"
              class="rounded-xl border border-slate-200 px-3 py-2 text-sm text-slate-700 outline-none focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
            />
          </label>
          <label class="block">
            <span class="mb-1.5 block text-xs font-semibold text-slate-500">종료일</span>
            <input
              v-model="endDate"
              type="date"
              :min="startDate || dataMinDate"
              :max="dataMaxDate"
              class="rounded-xl border border-slate-200 px-3 py-2 text-sm text-slate-700 outline-none focus:border-blue-300 focus:ring-2 focus:ring-blue-100"
            />
          </label>
          <button
            v-if="startDate || endDate"
            class="rounded-xl px-3 py-2 text-sm font-medium text-slate-500 transition hover:bg-slate-100"
            @click="resetRange"
          >
            전체 기간
          </button>
        </div>
      </div>

      <!-- 요약 카드 -->
      <div class="mb-5 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
          <p class="text-xs font-medium text-slate-400">최근가</p>
          <p class="mt-1 text-lg font-bold text-slate-900">{{ formatPrice(stats.latest) }}</p>
        </div>
        <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
          <p class="text-xs font-medium text-slate-400">기간 변동률</p>
          <p
            class="mt-1 text-lg font-bold"
            :class="
              stats.changePct > 0
                ? 'text-rose-500'
                : stats.changePct < 0
                  ? 'text-blue-500'
                  : 'text-slate-900'
            "
          >
            {{ formatPct(stats.changePct) }}
          </p>
        </div>
        <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
          <p class="text-xs font-medium text-slate-400">기간 최고</p>
          <p class="mt-1 text-lg font-bold text-slate-900">{{ formatPrice(stats.high) }}</p>
        </div>
        <div class="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-slate-100">
          <p class="text-xs font-medium text-slate-400">기간 최저</p>
          <p class="mt-1 text-lg font-bold text-slate-900">{{ formatPrice(stats.low) }}</p>
        </div>
      </div>

      <!-- 차트 -->
      <div class="rounded-3xl bg-white p-5 shadow-sm ring-1 ring-slate-100">
        <p class="mb-4 text-sm font-semibold text-slate-600">
          {{ currentAsset.label }} 가격 추이
          <span class="font-normal text-slate-400">(USD / oz)</span>
        </p>
        <div v-if="isInvalidRange" class="py-16 text-center text-sm text-rose-400">
          시작일이 종료일보다 늦어요. 다시 선택해 주세요.
        </div>
        <div v-else-if="filtered.length === 0" class="py-16 text-center text-sm text-slate-400">
          선택한 기간에 데이터가 없어요.
        </div>
        <div v-else class="h-80">
          <Line :data="chartData" :options="chartOptions" />
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Filler,
} from 'chart.js'
import type { ChartData, ChartOptions } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler)

type PricePoint = { date: string; close: number }
type AssetKey = 'gold' | 'silver'

const assetOptions: { value: AssetKey; label: string; color: string }[] = [
  { value: 'gold', label: '금', color: '#D4A017' },
  { value: 'silver', label: '은', color: '#94A3B8' },
]

const asset = ref<AssetKey>('gold')
const startDate = ref('')
const endDate = ref('')
const isLoading = ref(true)
const series = ref<Record<AssetKey, PricePoint[]>>({ gold: [], silver: [] })

const currentAsset = computed(
  () => assetOptions.find((o) => o.value === asset.value) ?? assetOptions[0]!,
)

const allPoints = computed(() => series.value[asset.value])
const dataMinDate = computed(() => allPoints.value[0]?.date ?? '')
const dataMaxDate = computed(() => allPoints.value[allPoints.value.length - 1]?.date ?? '')

const isInvalidRange = computed(
  () => Boolean(startDate.value) && Boolean(endDate.value) && startDate.value > endDate.value,
)

const filtered = computed(() =>
  allPoints.value.filter((p) => {
    if (startDate.value && p.date < startDate.value) return false
    if (endDate.value && p.date > endDate.value) return false
    return true
  }),
)

const stats = computed(() => {
  const pts = filtered.value
  if (pts.length === 0) return { latest: null, changePct: 0, high: null, low: null }
  const closes = pts.map((p) => p.close)
  const first = closes[0] ?? 0
  const latest = closes[closes.length - 1] ?? 0
  return {
    latest,
    changePct: first ? ((latest - first) / first) * 100 : 0,
    high: Math.max(...closes),
    low: Math.min(...closes),
  }
})

const chartData = computed<ChartData<'line'>>(() => ({
  labels: filtered.value.map((p) => p.date),
  datasets: [
    {
      label: currentAsset.value.label,
      data: filtered.value.map((p) => p.close),
      borderColor: currentAsset.value.color,
      backgroundColor: currentAsset.value.color + '22',
      borderWidth: 2,
      pointRadius: filtered.value.length <= 60 ? 3 : 0,
      pointHoverRadius: 5,
      tension: 0.25,
      fill: true,
    },
  ],
}))

const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: { mode: 'index', intersect: false },
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (ctx) => `${formatPrice(ctx.parsed.y ?? null)}`,
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: { maxTicksLimit: 8, color: '#94A3B8', font: { size: 11 } },
    },
    y: {
      grid: { color: '#F1F5F9' },
      ticks: { color: '#94A3B8', font: { size: 11 } },
    },
  },
}

function formatPrice(v: number | null): string {
  if (v === null) return '-'
  return '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function formatPct(v: number): string {
  const sign = v > 0 ? '+' : ''
  return `${sign}${v.toFixed(2)}%`
}

function resetRange() {
  startDate.value = ''
  endDate.value = ''
}

onMounted(async () => {
  try {
    const [gold, silver] = await Promise.all([
      fetch('/data/gold.json').then((r) => r.json()),
      fetch('/data/silver.json').then((r) => r.json()),
    ])
    series.value = { gold, silver }
  } catch {
    series.value = { gold: [], silver: [] }
  } finally {
    isLoading.value = false
  }
})
</script>
