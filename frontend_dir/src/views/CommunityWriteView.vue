<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-24 pb-20">
    <main class="mx-auto max-w-4xl px-5">
      <div class="mb-8 flex justify-end">
        <button
          class="text-sm font-bold cursor-pointer text-slate-500 transition hover:text-slate-900"
          @click="router.push('/financelounge?tab=community')"
        >
          목록으로 →
        </button>
      </div>

      <section class="mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight text-slate-900">
          {{ isEdit ? '게시글 수정' : '새 게시글 작성' }}
        </h1>
        <p class="mt-3 text-base font-medium leading-7 text-slate-400">
          궁금한 점이나 공유하고 싶은 금융 이야기를 남겨주세요.
        </p>
      </section>

      <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">불러오는 중...</div>

      <form
        v-else
        class="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
        @submit.prevent="onSubmit"
      >
        <!-- 제목 -->
        <div class="border-b border-slate-100 px-6 py-5">
          <label class="mb-2 block text-sm font-bold text-slate-600"> 제목 </label>
          <input
            v-model="title"
            type="text"
            maxlength="100"
            placeholder="제목을 입력하세요"
            class="w-full rounded-xl border border-slate-200 bg-slate-50 px-4 py-3 text-base font-semibold text-slate-900 outline-none transition placeholder:text-slate-300 focus:border-blue-300 focus:bg-white focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <!-- 내용 -->
        <div class="px-6 py-5">
          <div class="mb-2 flex items-center justify-between">
            <label class="block text-sm font-bold text-slate-600"> 내용 </label>
            <span class="text-xs font-medium text-slate-300"> 자유롭게 작성해 주세요 </span>
          </div>

          <textarea
            v-model="content"
            rows="12"
            placeholder="내용을 입력하세요"
            class="min-h-[320px] w-full resize-none rounded-xl border border-slate-200 bg-slate-50 px-4 py-4 text-base leading-8 text-slate-800 outline-none transition placeholder:text-slate-300 focus:border-blue-300 focus:bg-white focus:ring-2 focus:ring-blue-100"
          ></textarea>
        </div>

        <div
          class="flex items-center justify-between border-t border-slate-100 bg-slate-50/70 px-6 py-3"
        >
          <p class="text-xs font-medium text-slate-400">작성한 내용은 커뮤니티에 공개돼요.</p>

          <div class="flex gap-2">
            <button
              type="button"
              class="rounded-lg border border-slate-200 bg-white px-5 py-2.5 text-sm font-bold text-slate-500 transition hover:border-slate-300 hover:text-slate-900"
              @click="goBack"
            >
              취소
            </button>

            <button
              type="submit"
              :disabled="isSubmitting"
              class="rounded-lg bg-slate-900 px-6 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-slate-800 active:scale-95 disabled:opacity-50"
            >
              {{ isSubmitting ? '저장 중...' : isEdit ? '수정 완료' : '등록하기' }}
            </button>
          </div>
        </div>
      </form>
    </main>
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
