<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pb-20 pt-8">
    <div class="mx-auto max-w-6xl px-6">
      <!-- 검색바 -->
      <form
        class="mx-auto flex max-w-4xl items-center gap-3 rounded-2xl bg-white px-7 py-5 shadow-sm ring-1 ring-slate-200/70 transition focus-within:ring-2 focus-within:ring-indigo-200"
        @submit.prevent="search"
      >
        <input
          v-model="query"
          type="text"
          placeholder="예·적금 정보를 영상으로 알아보세요"
          class="flex-1 bg-transparent text-lg text-slate-700 placeholder:text-slate-400 focus:outline-none"
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
            class="h-6 w-6"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
            />
          </svg>
        </button>
      </form>

      <!-- 결과 영역 -->
      <div class="mt-12">
        <!-- 로딩 -->
        <div v-if="isLoading" class="mt-16 text-center text-base text-slate-400">
          불러오는 중...
        </div>

        <!-- 결과 없음 안내 -->
        <div v-else-if="hasSearched && results.length === 0" class="mt-20 text-center">
          <p class="text-lg font-semibold text-slate-500">검색 결과가 없어요</p>
          <p class="mt-2 text-sm text-slate-400">다른 키워드로 다시 검색해 보세요.</p>
        </div>

        <!-- 결과 그리드 -->
        <div v-else>
          <p v-if="lastKeyword" class="mb-5 text-sm text-slate-400">
            <span class="font-semibold text-slate-600">'{{ lastKeyword }}'</span> 검색 결과
          </p>
          <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
            <VideoCard v-for="v in results" :key="v.videoId" v-bind="v" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
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

const query = ref('')
const results = ref<VideoItem[]>([])
const isLoading = ref(false)
const hasSearched = ref(false)
const lastKeyword = ref('')

// 검색 실행. keyword를 직접 받으면 입력창과 무관하게 검색할 수 있다(초기 자동검색용).
async function runSearch(keyword: string) {
  const q = keyword.trim()
  if (!q) return

  isLoading.value = true
  hasSearched.value = true
  try {
    const { data } = await api.get('/api/v1/videos/search/', { params: { q } })
    // 백엔드 응답(snake_case) → 화면용 camelCase로 정리 + 제목/채널 엔티티 디코딩
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

// 검색 버튼/엔터 → 입력창 값으로 검색
function search() {
  runSearch(query.value)
}

// 첫 진입 시 빈 화면 대신 기본 키워드로 한 번 채워준다(입력창은 비워 둠).
onMounted(() => {
  runSearch('예적금')
})
</script>
