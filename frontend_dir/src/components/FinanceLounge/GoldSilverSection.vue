<template>
  <div>
    <h1 class="text-4xl font-extrabold text-slate-900">금 · 은 가격</h1>
    <p class="my-3 text-base font-light text-slate-400">
      대표 안전자산의 가격 흐름을 기간별로 확인해보세요.
    </p>

    <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">불러오는 중...</div>

    <template v-else>
      <section class="mt-5 rounded-[2rem] bg-white/90 p-5 shadow-sm ring-1 ring-slate-100">
        <div class="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
          <div>
            <span class="mb-2 ml-2 block text-sm font-extrabold text-slate-800">자산</span>

            <div class="inline-flex rounded-full bg-slate-100 p-1">
              <button
                v-for="opt in assetOptions"
                :key="opt.value"
                class="rounded-full px-5 py-2 text-sm font-extrabold transition"
                :class="
                  asset === opt.value
                    ? 'bg-white text-slate-900 shadow-sm'
                    : 'text-slate-500 hover:text-slate-700'
                "
                @click="changeAsset(opt.value)"
              >
                {{ opt.label }}
              </button>
            </div>
          </div>

          <div>
            <span class="mb-2 block text-sm font-extrabold text-slate-800">기간</span>

            <div class="flex flex-wrap gap-2">
              <button
                v-for="range in rangeOptions"
                :key="range.value"
                class="rounded-full px-4 py-2 text-sm font-extrabold transition"
                :class="
                  selectedRange === range.value
                    ? 'bg-slate-900 text-white shadow-md'
                    : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'
                "
                @click="selectRange(range.value)"
              >
                {{ range.label }}
              </button>
            </div>

            <!-- 직접 기간 선택 -->
            <div class="mt-3 flex flex-wrap items-center gap-2">
              <input
                type="date"
                :min="dataMinDate"
                :max="endDate || dataMaxDate"
                :value="startDate"
                @change="onDateInput('start', $event)"
                class="rounded-full border border-slate-200 px-3 py-1.5 text-sm font-semibold text-slate-600 focus:border-slate-400 focus:outline-none"
              />
              <span class="text-sm font-bold text-slate-400">~</span>
              <input
                type="date"
                :min="startDate || dataMinDate"
                :max="dataMaxDate"
                :value="endDate"
                @change="onDateInput('end', $event)"
                class="rounded-full border border-slate-200 px-3 py-1.5 text-sm font-semibold text-slate-600 focus:border-slate-400 focus:outline-none"
              />
            </div>
          </div>
        </div>

        <div class="my-8 h-px bg-slate-100"></div>

        <!-- 요약 지표 -->
        <div class="grid grid-cols-2 gap-y-8 lg:grid-cols-4">
          <div class="px-2 lg:border-r lg:border-slate-100 lg:pr-8">
            <p class="text-sm font-extrabold text-slate-500">현재 가격</p>
            <p class="mt-3 text-2xl font-extrabold text-slate-950">
              {{ formatPrice(stats.latest) }}
            </p>
            <p class="mt-1 text-xs font-semibold text-slate-400">USD / oz</p>
          </div>

          <div class="px-2 lg:border-r lg:border-slate-100 lg:px-8">
            <p class="text-sm font-extrabold text-slate-500">선택 기간 변동률</p>
            <p
              class="mt-3 text-2xl font-extrabold"
              :class="
                stats.changePct > 0
                  ? 'text-rose-500'
                  : stats.changePct < 0
                    ? 'text-blue-500'
                    : 'text-slate-950'
              "
            >
              {{ formatPct(stats.changePct) }}
            </p>
            <p class="mt-1 text-xs font-semibold text-slate-400">
              {{ stats.changePct > 0 ? '상승' : stats.changePct < 0 ? '하락' : '변동 없음' }}
            </p>
          </div>

          <div class="px-2 lg:border-r lg:border-slate-100 lg:px-8">
            <p class="text-sm font-extrabold text-slate-500">기간 최고가</p>
            <p class="mt-3 text-2xl font-extrabold text-slate-950">
              {{ formatPrice(stats.high) }}
            </p>
            <p class="mt-1 text-xs font-semibold text-slate-400">선택 기간 기준</p>
          </div>

          <div class="px-2 lg:pl-8">
            <p class="text-sm font-extrabold text-slate-500">기간 최저가</p>
            <p class="mt-3 text-2xl font-extrabold text-slate-950">
              {{ formatPrice(stats.low) }}
            </p>
            <p class="mt-1 text-xs font-semibold text-slate-400">선택 기간 기준</p>
          </div>
        </div>
      </section>

      <!-- 차트 박스 -->
      <section class="mt-7 rounded-[2rem] bg-white/90 p-8 shadow-sm ring-1 ring-slate-100">
        <div class="mb-6 flex items-start justify-between gap-4">
          <div>
            <p class="text-xl font-extrabold text-slate-900">{{ currentAsset.label }} 가격 추이</p>
            <p class="mt-2 text-sm font-semibold text-slate-400">
              선택한 기간의 가격 변화를 USD/oz 기준으로 확인해보세요.
            </p>
          </div>

          <span class="mt-1 text-sm font-bold text-slate-400">(USD / oz)</span>
        </div>

        <div v-if="filtered.length === 0" class="py-16 text-center text-sm text-slate-400">
          선택한 기간에 데이터가 없어요.
        </div>

        <div v-else class="h-80">
          <Line :data="chartData" :options="chartOptions" />
        </div>
      </section>
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
type RangeKey = '1m' | '3m' | '6m' | '1y' | 'all'

const assetOptions: { value: AssetKey; label: string; color: string }[] = [
  { value: 'gold', label: '금', color: '#D4A017' },
  { value: 'silver', label: '은', color: '#94A3B8' },
]

const rangeOptions: { value: RangeKey; label: string }[] = [
  { value: '1m', label: '1개월' },
  { value: '3m', label: '3개월' },
  { value: '6m', label: '6개월' },
  { value: '1y', label: '1년' },
  { value: 'all', label: '전체' },
]

const asset = ref<AssetKey>('gold')
const selectedRange = ref<RangeKey | 'custom'>('all')
const startDate = ref('')
const endDate = ref('')
const isLoading = ref(true)

const series = ref<Record<AssetKey, PricePoint[]>>({
  gold: [],
  silver: [],
})

const currentAsset = computed(
  () => assetOptions.find((o) => o.value === asset.value) ?? assetOptions[0]!,
)

const allPoints = computed(() => series.value[asset.value])

const dataMinDate = computed(() => allPoints.value[0]?.date ?? '')
const dataMaxDate = computed(() => allPoints.value[allPoints.value.length - 1]?.date ?? '')

const filtered = computed(() =>
  allPoints.value.filter((p) => {
    if (startDate.value && p.date < startDate.value) return false
    if (endDate.value && p.date > endDate.value) return false
    return true
  }),
)

const stats = computed(() => {
  const pts = filtered.value
  if (pts.length === 0) {
    return { latest: null, changePct: 0, high: null, low: null }
  }

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
      backgroundColor: `${currentAsset.value.color}22`,
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
        label: (ctx) => formatPrice(ctx.parsed.y ?? null),
      },
    },
  },
  scales: {
    x: {
      grid: { display: false },
      ticks: {
        maxTicksLimit: 8,
        color: '#94A3B8',
        font: { size: 11 },
      },
    },
    y: {
      grid: { color: '#F1F5F9' },
      ticks: {
        color: '#94A3B8',
        font: { size: 11 },
      },
    },
  },
}

function changeAsset(value: AssetKey) {
  asset.value = value
  // 직접 선택한 기간은 자산을 바꿔도 유지한다.
  const range = selectedRange.value
  if (range !== 'custom') {
    selectRange(range)
  }
}

function onDateInput(which: 'start' | 'end', e: Event) {
  const value = (e.target as HTMLInputElement).value
  if (which === 'start') startDate.value = value
  else endDate.value = value

  // 시작일이 종료일보다 뒤면 두 값을 맞춰 빈 결과를 막는다.
  if (startDate.value && endDate.value && startDate.value > endDate.value) {
    if (which === 'start') endDate.value = startDate.value
    else startDate.value = endDate.value
  }

  // 프리셋 버튼 선택 해제(직접 선택 상태)
  selectedRange.value = 'custom'
}

function selectRange(range: RangeKey) {
  selectedRange.value = range

  endDate.value = dataMaxDate.value

  if (range === 'all') {
    startDate.value = ''
    endDate.value = ''
    return
  }

  startDate.value = getPastDate(dataMaxDate.value, range)
}

function getPastDate(baseDate: string, range: RangeKey): string {
  if (!baseDate) return ''

  const date = new Date(baseDate)

  if (range === '1m') date.setMonth(date.getMonth() - 1)
  if (range === '3m') date.setMonth(date.getMonth() - 3)
  if (range === '6m') date.setMonth(date.getMonth() - 6)
  if (range === '1y') date.setFullYear(date.getFullYear() - 1)

  return date.toISOString().slice(0, 10)
}

function formatPrice(v: number | null): string {
  if (v === null) return '-'

  return (
    '$' +
    v.toLocaleString('en-US', {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    })
  )
}

function formatPct(v: number): string {
  const sign = v > 0 ? '+' : ''
  return `${sign}${v.toFixed(2)}%`
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
