<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pb-20 pt-8">
    <div class="mx-auto max-w-4xl px-6">
      <!-- 뒤로 -->
      <button
        class="mb-5 inline-flex items-center gap-1 text-sm font-medium text-slate-500 transition hover:text-slate-800"
        @click="goBack"
      >
        ← 뒤로
      </button>

      <!-- 로딩 -->
      <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">불러오는 중...</div>

      <!-- 없음 -->
      <div v-else-if="notFound" class="mt-20 text-center">
        <p class="text-lg font-semibold text-slate-500">영상을 찾을 수 없어요</p>
        <p class="mt-2 text-sm text-slate-400">삭제되었거나 잘못된 주소일 수 있어요.</p>
      </div>

      <!-- 재생 + 정보 -->
      <div v-else-if="video">
        <!-- iframe 플레이어 (16:9) -->
        <div class="overflow-hidden rounded-2xl bg-black shadow-lg ring-1 ring-slate-200">
          <div class="aspect-video">
            <iframe
              :src="`https://www.youtube.com/embed/${video.videoId}`"
              class="h-full w-full"
              title="YouTube video player"
              frameborder="0"
              allow="
                accelerometer;
                autoplay;
                clipboard-write;
                encrypted-media;
                gyroscope;
                picture-in-picture;
                web-share;
              "
              allowfullscreen
            ></iframe>
          </div>
        </div>

        <!-- 제목·채널·업로드일 -->
        <div class="mt-6 rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200/70">
          <h1 class="text-2xl font-extrabold leading-snug text-slate-900">{{ video.title }}</h1>
          <div class="mt-3 flex items-center justify-between gap-2 text-sm">
            <div class="flex items-center gap-2">
              <span class="font-semibold text-slate-700">{{ video.channelName }}</span>
              <span class="text-slate-300">·</span>
              <span class="text-slate-400">{{ formattedDate }}</span>
            </div>
            <!-- 영상 찜하기 (상품 상세의 찜 버튼과 같은 토글 디자인) -->
            <button
              @click="toggleFavorite"
              :aria-pressed="isFavorite"
              class="flex shrink-0 items-center gap-1.5 rounded-full border px-3.5 py-1.5 text-sm font-bold transition active:scale-95"
              :class="
                isFavorite
                  ? 'border-blue-300 bg-blue-50 text-blue-600'
                  : 'border-slate-200 bg-white text-slate-500 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-600'
              "
            >
              찜하기 {{ isFavorite ? '♥' : '♡' }}
            </button>
          </div>
          <p
            v-if="video.description"
            class="mt-5 max-h-60 overflow-y-auto whitespace-pre-line border-t border-slate-100 pt-5 text-sm leading-relaxed text-slate-500"
          >
            {{ video.description }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { decodeHtmlEntities } from '@/utils/decodeHtml'
import { useVideoFavoritesStore } from '@/stores/videoFavorites'

// 라우트 파라미터(/videos/:videoId)를 props로 받는다 (router에서 props: true)
const props = defineProps<{ videoId: string }>()
const router = useRouter()
const favoritesStore = useVideoFavoritesStore()

interface VideoDetail {
  videoId: string
  title: string
  channelName: string
  thumbnailUrl: string
  publishedAt: string
  description: string
}

const video = ref<VideoDetail | null>(null)
const isLoading = ref(false)
const notFound = ref(false)

// 영상 상세 응답엔 찜 여부가 없으므로(YouTube 프록시), 내 찜 목록에 이 영상이 있는지로 판단한다.
const isFavorite = computed(() => favoritesStore.isFavorited(props.videoId))

// ISO 날짜 → "2026.06.22 업로드"
const formattedDate = computed(() => {
  if (!video.value) return ''
  const d = new Date(video.value.publishedAt)
  if (isNaN(d.getTime())) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day} 업로드`
})

function goBack() {
  router.back()
}

// 하트 클릭 → 찜 등록/해제 토글. 등록엔 목록 표시용 정보(썸네일·채널 등)를 함께 보낸다.
async function toggleFavorite() {
  if (!video.value) return
  try {
    if (isFavorite.value) {
      await favoritesStore.removeVideoFavorite(video.value.videoId)
    } else {
      await favoritesStore.addVideoFavorite({
        video_id: video.value.videoId,
        title: video.value.title,
        thumbnail_url: video.value.thumbnailUrl,
        channel_name: video.value.channelName,
      })
    }
  } catch {
    alert('찜하기 처리에 실패했어요. 다시 시도해주세요.')
  }
}

onMounted(async () => {
  isLoading.value = true
  // 하트 상태 판단용 내 찜 목록 — 영상 로드와 무관하게 받아온다(실패해도 페이지는 그대로).
  favoritesStore.fetchVideoFavorites().catch(() => {})
  try {
    const { data } = await api.get(`/api/v1/videos/${props.videoId}/`)
    video.value = {
      videoId: data.video_id,
      title: decodeHtmlEntities(data.title),
      channelName: decodeHtmlEntities(data.channel_name),
      thumbnailUrl: data.thumbnail_url ?? '',
      publishedAt: data.published_at,
      description: decodeHtmlEntities(data.description ?? ''),
    }
  } catch (e: any) {
    if (e?.response?.status === 404) notFound.value = true
    else alert('영상을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
})
</script>
