<template>
  <div>
    <h1 class="text-4xl font-extrabold text-slate-900">금융 TV</h1>
    <p class="my-3 text-base font-light text-slate-400">
      예·적금 상품, 금리, 우대조건까지 어려운 금융 정보를 영상으로 쉽게 확인해보세요.
    </p>
    <form
      class="flex items-center gap-3 rounded-2xl bg-white px-7 py-5 shadow-sm ring-1 ring-slate-200/70 transition focus-within:ring-2 focus-within:ring-indigo-200"
      @submit.prevent="search"
    >
      <input
        v-model="query"
        type="text"
        placeholder="궁금한 예·적금 키워드를 입력해보세요"
        class="flex-1 bg-transparent text-base text-slate-700 placeholder:text-slate-400 focus:outline-none"
      />
      <button
        type="submit"
        aria-label="검색"
        class="shrink-0 text-slate-400 transition hover:text-indigo-500"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke-width="2"
          stroke="currentColor"
          class="h-5 w-5"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
          />
        </svg>
      </button>
    </form>

    <div class="mt-4 flex flex-wrap items-center justify-between gap-2">
      <div class="flex flex-wrap items-center gap-2">
        <span class="text-sm font-semibold text-slate-500">추천 키워드</span>
        <button
          v-for="kw in keywords"
          :key="kw"
          @click="runSearch(kw)"
          class="rounded-full bg-white px-4 py-1.5 text-sm font-medium text-slate-600 shadow-sm ring-1 ring-slate-200 hover:bg-blue-50 hover:text-blue-600"
        >
          #{{ kw }}
        </button>
      </div>
      <div class="inline-flex rounded-full bg-slate-100 p-1">
        <button
          v-for="opt in orderOptions"
          :key="opt.value"
          @click="changeOrder(opt.value)"
          class="rounded-full px-4 py-1.5 text-sm font-semibold transition"
          :class="
            order === opt.value
              ? 'bg-white text-slate-900 shadow-sm'
              : 'text-slate-500 hover:text-slate-700'
          "
        >
          {{ opt.label }}
        </button>
      </div>
    </div>

    <div class="mt-8">
      <div v-if="isLoading" class="mt-12 text-center text-base text-slate-400">
        영상을 불러오는 중입니다. 잠시만 기다려주세요 !
      </div>

      <div v-else-if="hasSearched && results.length === 0" class="mt-16 text-center">
        <p class="text-base font-semibold text-slate-500">검색 결과가 없어요</p>
        <p class="mt-2 text-sm text-slate-400">다른 키워드로 다시 검색해 보세요.</p>
      </div>

      <div v-else>
        <p v-if="lastKeyword" class="mb-4 text-sm text-slate-400">
          <span class="font-semibold text-slate-600">'{{ lastKeyword }}'</span> 관련 영상을
          모아봤어요
        </p>
        <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          <VideoCard v-for="v in results" :key="v.videoId" v-bind="v" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '@/api'
import VideoCard from '@/components/Video/VideoCard.vue'
import { decodeHtmlEntities } from '@/utils/decodeHtml'

interface VideoItem {
  videoId: string
  title: string
  channelName: string
  thumbnailUrl: string
  publishedAt: string
}

const keywords = ['파킹통장', '우대금리', '청년도약계좌', '예금자보호']
const orderOptions = [
  { label: '정확도순', value: 'relevance' },
  { label: '최신순', value: 'date' },
  { label: '조회수순', value: 'viewCount' },
]

const query = ref('')
const results = ref<VideoItem[]>([])
const isLoading = ref(false)
const hasSearched = ref(false)
const lastKeyword = ref('')
const order = ref('relevance')

async function runSearch(keyword: string) {
  const q = keyword.trim()
  if (!q) return
  isLoading.value = true
  hasSearched.value = true
  try {
    const { data } = await api.get('/api/v1/videos/search/', {
      params: { q, max_results: 9, order: order.value },
    })
    results.value = data.map((item: any) => ({
      videoId: item.video_id,
      title: decodeHtmlEntities(item.title),
      channelName: decodeHtmlEntities(item.channel_name),
      thumbnailUrl: item.thumbnail_url,
      publishedAt: item.published_at,
    }))
    lastKeyword.value = q
  } catch {
    alert('영상을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
}

function changeOrder(value: string) {
  order.value = value
  if (lastKeyword.value) runSearch(lastKeyword.value)
}

function search() {
  runSearch(query.value)
}

</script>
