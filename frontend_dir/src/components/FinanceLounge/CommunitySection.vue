<template>
  <div>
    <div class="mb-4">
      <div class="flex items-end justify-between gap-4">
        <div>
          <h1 class="text-4xl font-extrabold text-slate-900">커뮤니티</h1>
          <p class="my-1 text-base font-light text-slate-400">
            금융 정보와 궁금한 점을 자유롭게 나눠보세요.
          </p>
        </div>

        <button
          v-if="isAuthenticated"
          class="rounded-lg bg-slate-900 px-6 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-slate-800 active:scale-95 disabled:opacity-50"
          @click="router.push({ name: 'community-write' })"
        >
          글쓰기
        </button>
      </div>
    </div>

    <div class="overflow-hidden rounded-3xl bg-white shadow-sm ring-1 ring-slate-100">
      <table class="w-full table-fixed">
        <thead>
          <tr class="border-b border-slate-100 bg-slate-50/60 text-sm font-semibold text-slate-400">
            <th class="w-16 py-3.5 pl-6 pr-3 text-left">번호</th>
            <th class="py-3.5 pr-3 text-left">제목</th>
            <th class="w-24 py-3.5 pr-3 text-left">작성자</th>
            <th class="w-32 py-3.5 pr-6 text-left">날짜</th>
          </tr>
        </thead>
        <tbody v-if="!isLoading">
          <tr
            v-for="post in posts"
            :key="post.id"
            class="group cursor-pointer border-b border-slate-100 transition last:border-0 hover:bg-blue-50/40"
            @click="router.push(`/community/${post.id}`)"
          >
            <td class="py-4 pl-6 pr-3 text-base text-slate-300">{{ post.id }}</td>
            <td class="py-4 pr-3">
              <div class="flex items-center gap-1 overflow-hidden">
                <span
                  class="min-w-0 truncate text-base font-semibold text-slate-800 group-hover:text-blue-600"
                >
                  {{ post.title }}
                </span>
                <span
                  v-if="post.commentCount > 0"
                  class="shrink-0 text-sm font-medium text-blue-400"
                >
                  [{{ post.commentCount }}]
                </span>
              </div>
            </td>
            <td class="truncate py-4 pr-3 text-base text-slate-500">{{ post.authorNickname }}</td>
            <td class="py-4 pr-6 text-sm text-slate-400">{{ post.createdAt }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="isLoading" class="px-6 py-16 text-center text-base text-slate-400">
        불러오는 중...
      </div>
      <div v-else-if="posts.length === 0" class="px-6 py-16 text-center text-base text-slate-400">
        아직 게시글이 없어요. 첫 번째 글을 작성해보세요!
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { Post, PostApi } from '@/types/community'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const posts = ref<Post[]>([])
const isLoading = ref(false)

async function fetchPosts() {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/v1/community/posts/')
    posts.value = data.map((p: PostApi) => ({
      id: p.id,
      title: p.title,
      authorId: p.author_id,
      authorNickname: p.author_nickname,
      commentCount: p.comment_count,
      createdAt: (p.created_at ?? '').slice(0, 10),
    }))
  } catch {
    alert('게시글을 불러오는 데 실패했어요.')
  } finally {
    isLoading.value = false
  }
}

onMounted(fetchPosts)
</script>
