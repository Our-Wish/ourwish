<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-24 pb-16">
    <div class="mx-auto max-w-3xl px-4">
      <!-- 뒤로 -->
      <button
        class="mb-6 inline-flex items-center gap-1 text-sm font-bold text-slate-500 transition hover:text-slate-800"
        @click="goBack"
      >
        ← 목록
      </button>

      <div class="mb-8">
        <h1 class="text-4xl font-extrabold text-slate-900">
          {{ isEdit ? '글 수정' : '글쓰기' }}
        </h1>
        <p class="my-3 text-base font-light text-slate-400">
          금융 정보와 궁금한 점을 자유롭게 공유해보세요.
        </p>
      </div>

      <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">불러오는 중...</div>

      <form
        v-else
        class="rounded-[2rem] bg-white/90 p-8 shadow-sm ring-1 ring-slate-100"
        @submit.prevent="onSubmit"
      >
        <!-- 제목 -->
        <div class="mb-6">
          <label class="mb-2 block text-sm font-extrabold text-slate-700">제목</label>
          <input
            v-model="title"
            type="text"
            maxlength="100"
            placeholder="제목을 입력하세요"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50/60 px-5 py-4 text-base font-semibold text-slate-800 outline-none transition placeholder:text-slate-300 focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-100"
          />
        </div>

        <!-- 본문 -->
        <div>
          <label class="mb-2 block text-sm font-extrabold text-slate-700">내용</label>
          <textarea
            v-model="content"
            rows="13"
            placeholder="내용을 입력하세요"
            class="w-full resize-none rounded-2xl border border-slate-200 bg-slate-50/60 px-5 py-4 text-base leading-relaxed text-slate-800 outline-none transition placeholder:text-slate-300 focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-100"
          ></textarea>
        </div>

        <div class="mt-8 flex justify-end gap-2 border-t border-slate-100 pt-6">
          <button
            type="button"
            class="rounded-full px-5 py-2.5 text-sm font-bold text-slate-500 transition hover:bg-slate-100"
            @click="goBack"
          >
            취소
          </button>

          <button
            type="submit"
            :disabled="isSubmitting"
            class="rounded-full bg-slate-900 px-7 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-slate-800 active:scale-95 disabled:opacity-50"
          >
            {{ isSubmitting ? '저장 중...' : isEdit ? '수정 완료' : '등록' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

// /community/:id/edit 일 때만 id가 들어온다 (작성은 undefined)
const props = defineProps<{ id?: string }>()
const router = useRouter()

const isEdit = computed(() => Boolean(props.id))

const title = ref('')
const content = ref('')
const isLoading = ref(false)
const isSubmitting = ref(false)

function goBack() {
  router.back()
}

// 수정 모드면 기존 글을 불러와 폼에 채운다
onMounted(async () => {
  if (!isEdit.value) return
  isLoading.value = true
  try {
    const { data } = await api.get(`/api/v1/community/posts/${props.id}/`)
    title.value = data.title
    content.value = data.content
  } catch {
    alert('글을 불러오는 데 실패했어요.')
    router.replace({ name: 'community' })
  } finally {
    isLoading.value = false
  }
})

async function onSubmit() {
  if (!title.value.trim()) {
    alert('제목을 입력해 주세요.')
    return
  }
  if (!content.value.trim()) {
    alert('내용을 입력해 주세요.')
    return
  }

  isSubmitting.value = true
  const payload = { title: title.value, content: content.value }
  try {
    if (isEdit.value) {
      await api.patch(`/api/v1/community/posts/${props.id}/`, payload)
      router.replace(`/community/${props.id}`)
    } else {
      const { data } = await api.post('/api/v1/community/posts/', payload)
      router.replace(`/community/${data.id}`)
    }
  } catch {
    alert('저장에 실패했어요. 다시 시도해 주세요.')
  } finally {
    isSubmitting.value = false
  }
}
</script>
