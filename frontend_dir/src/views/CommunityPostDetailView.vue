<template>
  <div class="min-h-screen pt-24 pb-24">
    <main class="mx-auto max-w-4xl px-8">
      <div class="mb-8 flex justify-end">
        <button
          class="text-sm font-bold cursor-pointer text-slate-500 transition hover:text-slate-900"
          @click="router.push('/financelounge?tab=community')"
        >
          목록으로 →
        </button>
      </div>

      <div v-if="isLoading" class="mt-20 text-center text-base text-slate-400">
        불러오는 중입니다.
      </div>

      <div v-else-if="notFound" class="mt-20 text-center">
        <p class="text-lg font-semibold text-slate-500">게시글을 찾을 수 없어요</p>
        <p class="mt-2 text-sm text-slate-400">삭제되었거나 잘못된 주소일 수 있어요.</p>
      </div>

      <template v-else-if="post">
        <article>
          <h1 class="text-4xl font-extrabold tracking-tight text-slate-900">
            {{ post.title }}
          </h1>

          <div class="mt-4 flex items-center justify-between">
            <div class="flex items-center gap-2 text-base">
              <span class="font-bold text-slate-700">{{ post.authorNickname }}</span>
              <span class="text-slate-300">|</span>
              <span class="font-medium text-slate-400">{{ formatDate(post.createdAt) }}</span>
            </div>

            <div v-if="isMine(post.authorId)" class="flex items-center gap-3 text-sm">
              <button
                class="font-bold text-slate-400 transition hover:text-slate-900"
                @click="router.push(`/community/${post.id}/edit`)"
              >
                수정
              </button>
              <span class="text-slate-200">|</span>
              <button
                class="font-bold text-slate-400 transition hover:text-rose-500"
                @click="onDeletePost"
              >
                삭제
              </button>
            </div>
          </div>

          <div class="mt-5 border-t border-slate-200 pt-10">
            <p class="text-lg leading-9 break-words whitespace-pre-line text-slate-700">
              {{ post.content }}
            </p>
          </div>
        </article>
        <section class="mt-16 border-t border-slate-200 pt-8">
          <h2 class="mb-6 text-xl font-extrabold text-slate-900">
            댓글 <span class="text-blue-500">{{ post.comments.length }}</span>
          </h2>

          <div v-if="isAuthenticated" class="mb-8">
            <div
              class="relative rounded-xl border border-slate-200 bg-slate-50/70 transition focus-within:border-slate-400 focus-within:bg-white focus-within:ring-2 focus-within:ring-slate-100"
            >
              <textarea
                v-model="newComment"
                rows="3"
                placeholder="댓글을 입력하세요"
                class="w-full resize-none bg-transparent px-4 pt-4 pb-1 text-sm leading-6 text-slate-800 outline-none placeholder:text-slate-300"
              ></textarea>

              <button
                :disabled="isPosting"
                class="absolute right-3 bottom-3 rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white transition hover:bg-slate-800 disabled:opacity-50"
                @click="onCreateComment"
              >
                {{ isPosting ? '등록 중...' : '등록' }}
              </button>
            </div>
          </div>

          <ul v-if="post.comments.length > 0" class="divide-y divide-slate-200">
            <li v-for="c in post.comments" :key="c.id" class="py-5">
              <div class="flex items-center justify-between gap-4">
                <div class="flex items-center gap-2 text-sm">
                  <span class="font-bold text-slate-700">{{ c.authorNickname }}</span>
                  <span class="text-slate-300">·</span>
                  <span class="text-slate-400">{{ formatDate(c.createdAt) }}</span>
                </div>

                <div v-if="isMine(c.authorId)" class="flex items-center gap-2 text-xs">
                  <button
                    v-if="editingId !== c.id"
                    class="font-bold text-slate-400 transition hover:text-slate-900"
                    @click="startEdit(c)"
                  >
                    수정
                  </button>
                  <span v-if="editingId !== c.id" class="text-slate-200">|</span>
                  <button
                    v-if="editingId !== c.id"
                    class="font-bold text-slate-400 transition hover:text-rose-500"
                    @click="onDeleteComment(c.id)"
                  >
                    삭제
                  </button>
                </div>
              </div>

              <div v-if="editingId === c.id" class="mt-3">
                <div class="relative rounded-xl border border-slate-200 bg-slate-50/70">
                  <textarea
                    v-model="editText"
                    rows="3"
                    class="w-full resize-none bg-transparent px-4 pt-4 pb-14 text-sm leading-6 text-slate-800 outline-none"
                  ></textarea>

                  <div class="absolute right-3 bottom-3 flex gap-2">
                    <button
                      class="rounded-lg px-3 py-2 text-xs font-bold text-slate-500 hover:bg-slate-100"
                      @click="cancelEdit"
                    >
                      취소
                    </button>
                    <button
                      class="rounded-lg bg-slate-900 px-4 py-2 text-xs font-bold text-white hover:bg-slate-800"
                      @click="onUpdateComment(c.id)"
                    >
                      저장
                    </button>
                  </div>
                </div>
              </div>

              <div v-else class="mt-3 text-sm leading-7 text-slate-700">
                <CommentBody :content="c.content" />
              </div>
            </li>
          </ul>

          <p
            v-else
            class="rounded-xl bg-slate-50 py-10 text-center text-sm font-medium text-slate-400"
          >
            첫 댓글을 남겨보세요.
          </p>
        </section>
      </template>
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import CommentBody from '@/components/Community/CommentBody.vue'
import { useAuthStore } from '@/stores/auth'
import type { Comment, PostDetail } from '@/types/community'

const props = defineProps<{ id: string }>()
const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const post = ref<PostDetail | null>(null)
const isLoading = ref(false)
const notFound = ref(false)

const newComment = ref('')
const isPosting = ref(false)

const editingId = ref<number | null>(null)
const editText = ref('')

// 내 글/댓글 여부 — authorId와 로그인한 member.id 비교
function isMine(authorId: number) {
  return authStore.user?.id === authorId
}

function formatDate(iso: string) {
  const d = new Date(iso)
  if (isNaN(d.getTime())) return ''
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  const hh = String(d.getHours()).padStart(2, '0')
  const mm = String(d.getMinutes()).padStart(2, '0')
  return `${y}.${m}.${day} ${hh}:${mm}`
}

function mapComment(c: any): Comment {
  return {
    id: c.id,
    authorId: c.author_id,
    authorNickname: c.author_nickname,
    content: c.content,
    createdAt: c.created_at,
  }
}

async function fetchPost() {
  isLoading.value = true
  try {
    const { data } = await api.get(`/api/v1/community/posts/${props.id}/`)
    post.value = {
      id: data.id,
      title: data.title,
      content: data.content,
      authorId: data.author_id,
      authorNickname: data.author_nickname,
      comments: (data.comments ?? []).map(mapComment),
      createdAt: data.created_at,
    }
  } catch (e: any) {
    if (e?.response?.status === 404) notFound.value = true
    else alert('게시글을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
}

async function onDeletePost() {
  if (!post.value) return
  if (!confirm('이 글을 삭제할까요?')) return
  try {
    await api.delete(`/api/v1/community/posts/${post.value.id}/`)
    router.replace('/financelounge?tab=community')
  } catch {
    alert('삭제에 실패했어요.')
  }
}

async function onCreateComment() {
  if (!post.value) return
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력해 주세요.')
    return
  }
  isPosting.value = true
  try {
    const { data } = await api.post(`/api/v1/community/posts/${post.value.id}/comments/`, {
      content: newComment.value,
    })
    post.value.comments.push(mapComment(data))
    newComment.value = ''
  } catch {
    alert('댓글 등록에 실패했어요.')
  } finally {
    isPosting.value = false
  }
}

function startEdit(c: Comment) {
  editingId.value = c.id
  editText.value = c.content
}

function cancelEdit() {
  editingId.value = null
  editText.value = ''
}

async function onUpdateComment(commentId: number) {
  if (!editText.value.trim()) {
    alert('댓글 내용을 입력해 주세요.')
    return
  }
  try {
    const { data } = await api.patch(`/api/v1/community/comments/${commentId}/`, {
      content: editText.value,
    })
    const idx = post.value?.comments.findIndex((c) => c.id === commentId) ?? -1
    if (post.value && idx !== -1) post.value.comments[idx] = mapComment(data)
    cancelEdit()
  } catch {
    alert('댓글 수정에 실패했어요.')
  }
}

async function onDeleteComment(commentId: number) {
  if (!confirm('이 댓글을 삭제할까요?')) return
  try {
    await api.delete(`/api/v1/community/comments/${commentId}/`)
    if (post.value) post.value.comments = post.value.comments.filter((c) => c.id !== commentId)
  } catch {
    alert('댓글 삭제에 실패했어요.')
  }
}

onMounted(fetchPost)
</script>
