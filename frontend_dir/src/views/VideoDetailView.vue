<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pb-20 pt-8">
    <div class="mx-auto max-w-4xl px-6">
      <!-- 뒤로가기 -->
      <button
        class="mb-8 inline-flex items-center gap-1 rounded-full px-3 py-2 text-sm font-bold text-slate-500 transition hover:bg-white/70 hover:text-slate-800 hover:shadow-sm"
        @click="goBack"
      >
        ← 금융TV로 돌아가기
      </button>

      <!-- 로딩 -->
      <div
        v-if="isLoading"
        class="mt-24 rounded-4xl bg-white/70 px-6 py-16 text-center shadow-sm ring-1 ring-slate-200/70"
      >
        <p class="text-base font-semibold text-slate-500">영상을 불러오는 중이에요.</p>
        <p class="mt-2 text-sm text-slate-400">잠시만 기다려주세요.</p>
      </div>

      <!-- 없음 -->
      <div
        v-else-if="notFound"
        class="mt-24 rounded-4xl bg-white/70 px-6 py-16 text-center shadow-sm ring-1 ring-slate-200/70"
      >
        <p class="text-xl font-extrabold text-slate-900">영상을 찾을 수 없어요</p>
        <p class="mt-3 text-sm text-slate-400">삭제되었거나 잘못된 주소일 수 있어요.</p>

        <button
          class="mt-8 rounded-full bg-blue-600 px-6 py-3 text-sm font-bold text-white transition hover:bg-blue-700 active:scale-95"
          @click="goBack"
        >
          이전 페이지로 돌아가기
        </button>
      </div>

      <!-- 재생 + 정보 -->
      <div v-else-if="video">
        <!-- 영상 상단 정보 -->
        <div class="mb-6 flex items-start justify-between gap-6">
          <div class="min-w-0">
            <h1 class="text-3xl font-extrabold leading-snug text-slate-950">
              {{ video.title }}
            </h1>

            <div class="mt-4 flex flex-wrap items-center gap-2 text-sm">
              <span class="font-bold text-slate-700">
                {{ video.channelName }}
              </span>
              <span class="text-slate-300">·</span>
              <span class="font-medium text-slate-400">
                {{ formattedDate }}
              </span>
            </div>
          </div>

          <button
            @click="toggleFavorite"
            :aria-pressed="isFavorite"
            :disabled="isFavoriteSubmitting"
            class="mt-1 shrink-0 rounded-full px-4 py-2 text-sm font-bold transition active:scale-95 disabled:cursor-not-allowed disabled:opacity-60"
            :class="
              isFavorite
                ? 'bg-blue-600 text-white shadow-sm hover:bg-blue-700'
                : 'bg-white/80 text-slate-500 shadow-sm ring-1 ring-slate-200 hover:bg-blue-50 hover:text-blue-600 hover:ring-blue-100'
            "
          >
            {{ isFavorite ? '찜한 영상 ♥' : '찜하기 ♡' }}
          </button>
        </div>

        <!-- iframe 플레이어 -->
        <div class="overflow-hidden rounded-4xl bg-black shadow-xl ring-1 ring-slate-200">
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

        <!-- 영상 설명 -->
        <details v-if="video.description?.trim()" class="mt-6 border-t border-slate-200/70 pt-5">
          <summary
            class="cursor-pointer text-sm font-bold text-slate-500 transition hover:text-slate-800"
          >
            영상 설명 보기
          </summary>

          <p
            class="mt-4 max-h-60 overflow-y-auto whitespace-pre-line text-sm leading-7 text-slate-500"
          >
            {{ video.description }}
          </p>
        </details>
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

// 라우트 파라미터(/videos/:videoId)를 props로 받는다.
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
const isFavoriteSubmitting = ref(false)

// 영상 상세 응답엔 찜 여부가 없으므로 내 찜 목록 기준으로 판단한다.
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

// 하트 클릭 → 찜 등록/해제 토글
async function toggleFavorite() {
  if (!video.value || isFavoriteSubmitting.value) return

  isFavoriteSubmitting.value = true

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
  } finally {
    isFavoriteSubmitting.value = false
  }
}

onMounted(async () => {
  isLoading.value = true

  // 하트 상태 판단용 내 찜 목록
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
    if (e?.response?.status === 404) {
      notFound.value = true
    } else {
      alert('영상을 불러오는 데 실패했어요.')
    }
  } finally {
    isLoading.value = false
  }
})
</script>
