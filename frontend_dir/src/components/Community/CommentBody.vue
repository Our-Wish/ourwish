<template>
  <div>
    <p
      ref="textEl"
      class="text-sm leading-relaxed break-words whitespace-pre-line text-slate-600"
      :class="expanded ? '' : 'line-clamp-2'"
    >
      {{ content }}
    </p>
    <!-- 잘렸을 때(또는 펼친 상태)만 토글 노출 -->
    <button
      v-if="isOverflowing || expanded"
      class="mt-1 text-xs font-medium text-slate-400 transition hover:text-blue-600"
      @click="expanded = !expanded"
    >
      {{ expanded ? '접기' : '더보기' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from 'vue'

const props = defineProps<{ content: string }>()

const expanded = ref(false)
const isOverflowing = ref(false)
const textEl = ref<HTMLElement | null>(null)

// 접힌(line-clamp-2) 상태에서 실제 높이가 보이는 높이보다 크면 잘린 것
function checkOverflow() {
  const el = textEl.value
  if (!el) return
  isOverflowing.value = el.scrollHeight > el.clientHeight + 1
}

onMounted(async () => {
  await nextTick()
  checkOverflow()
})

// 내용이 바뀌면(수정 등) 다시 측정 — 펼친 상태에선 측정값이 무의미하므로 스킵
watch(
  () => props.content,
  async () => {
    if (expanded.value) return
    await nextTick()
    checkOverflow()
  },
)
</script>
