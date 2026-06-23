<template>
  <div>
    <h1 class="text-4xl font-extrabold text-slate-900">찜한 영상 관리</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      예·적금 공부에 도움이 됐던 영상을 다시 꺼내보세요.
    </p>

    <!-- 로딩 -->
    <div v-if="store.isLoading" class="mt-16 text-center text-base text-slate-400">
      불러오는 중...
    </div>

    <!-- 빈 상태 -->
    <div
      v-else-if="store.favorites.length === 0"
      class="mt-20 text-center text-base text-slate-300"
    >
      찜한 영상이 없어요.
    </div>

    <!-- 그리드 -->
    <div v-else class="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      <div
        v-for="video in store.favorites"
        :key="video.video_id"
        class="group flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60"
        @click="goDetail(video.video_id)"
      >
        <!-- 썸네일 (16:9 고정) -->
        <div class="aspect-video overflow-hidden bg-slate-100">
          <img
            :src="video.thumbnail_url"
            :alt="video.title"
            loading="lazy"
            class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
          />
        </div>

        <!-- 제목·채널·찜 해제 -->
        <div class="flex flex-1 flex-col p-4">
          <p class="line-clamp-2 text-sm font-bold leading-snug text-slate-900">
            {{ decodeHtmlEntities(video.title) }}
          </p>
          <div class="mt-auto flex items-center justify-between gap-2 pt-3">
            <p class="truncate text-xs font-medium text-slate-500">
              {{ decodeHtmlEntities(video.channel_name) }}
            </p>
            <!-- 찜 해제 (영상 상세의 찜 버튼과 같은 토글 디자인) -->
            <button
              @click.stop="removeFavorite(video.video_id)"
              :disabled="removingId === video.video_id"
              aria-label="찜 해제"
              class="flex shrink-0 items-center gap-1 rounded-full border border-blue-300 bg-blue-50 px-3 py-1 text-xs font-bold text-blue-600 transition hover:bg-blue-100 active:scale-95 disabled:opacity-50"
            >
              찜 ♥
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useVideoFavoritesStore } from '@/stores/videoFavorites'
import { decodeHtmlEntities } from '@/utils/decodeHtml'

const router = useRouter()
const store = useVideoFavoritesStore()

// 해제 처리 중인 영상 id (연타로 중복 DELETE 나가는 걸 막는다)
const removingId = ref<string | null>(null)

onMounted(() => store.fetchVideoFavorites())

function goDetail(videoId: string) {
  router.push({ name: 'video-detail', params: { videoId } })
}

async function removeFavorite(videoId: string) {
  if (removingId.value !== null) return
  removingId.value = videoId
  try {
    await store.removeVideoFavorite(videoId)
  } catch {
    alert('영상 찜 해제에 실패했어요.')
  } finally {
    removingId.value = null
  }
}
</script>
