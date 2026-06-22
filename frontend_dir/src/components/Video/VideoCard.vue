<template>
  <!-- ProductCard와 같은 둥근 흰 카드 + hover로 살짝 떠오르는 인터랙션 -->
  <div
    class="group flex cursor-pointer flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white transition hover:-translate-y-0.5 hover:border-blue-200 hover:shadow-lg hover:shadow-slate-200/60"
    @click="goDetail"
  >
    <!-- 썸네일 (16:9 고정) -->
    <div class="aspect-video overflow-hidden bg-slate-100">
      <img
        :src="thumbnailUrl"
        :alt="title"
        loading="lazy"
        class="h-full w-full object-cover transition duration-300 group-hover:scale-105"
      />
    </div>

    <!-- 제목·채널·날짜 -->
    <div class="flex flex-1 flex-col p-4">
      <p class="line-clamp-2 text-sm font-bold leading-snug text-slate-900">{{ title }}</p>
      <div class="mt-auto pt-3">
        <p class="truncate text-xs font-medium text-slate-500">{{ channelName }}</p>
        <p class="mt-0.5 text-xs text-slate-400">{{ formattedDate }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'

// 부모(VideoSearchView)에서 camelCase로 정리해 내려주는 값들
const props = defineProps<{
  videoId: string
  title: string
  channelName: string
  thumbnailUrl: string
  publishedAt: string
}>()

const router = useRouter()

// ISO 날짜("2026-06-22T05:15:11Z") → "2026.06.22"
const formattedDate = computed(() => {
  const d = new Date(props.publishedAt)
  if (isNaN(d.getTime())) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}.${m}.${day}`
})

function goDetail() {
  router.push({ name: 'video-detail', params: { videoId: props.videoId } })
}
</script>
