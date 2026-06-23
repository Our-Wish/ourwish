<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7] pt-24 pb-16">
    <div class="mx-auto max-w-3xl px-4">
      <!-- 헤더 -->
      <div class="mb-6">
        <p class="mb-1 text-sm font-bold tracking-widest text-blue-400">✦ OUR WISH</p>
        <div class="flex items-end justify-between">
          <div>
            <h1 class="text-3xl font-bold tracking-tight text-slate-900">커뮤니티</h1>
            <p class="mt-1 text-sm text-slate-400">금융 고민을 함께 나눠요</p>
          </div>
          <!-- 로그인한 사용자만 글쓰기 페이지로 이동 -->
          <button
            v-if="isAuthenticated"
            class="rounded-full bg-blue-500 px-5 py-2.5 text-base font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-600 active:scale-95"
            @click="router.push({ name: 'community-write' })"
          >
            글쓰기 +
          </button>
        </div>
      </div>

      <div class="overflow-hidden rounded-3xl bg-white shadow-sm ring-1 ring-slate-100">
        <!-- table-fixed + 전 열 좌측 정렬: 헤더와 데이터의 시작점(왼쪽)을 통일 -->
        <table class="w-full table-fixed">
          <thead>
            <tr
              class="border-b border-slate-100 bg-slate-50/60 text-sm font-semibold text-slate-400"
            >
              <th class="w-16 py-3.5 pr-3 pl-6 text-left">번호</th>
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
              <td class="py-4 pr-3 pl-6 text-base text-slate-300">{{ post.id }}</td>
              <td class="py-4 pr-3">
                <!-- 긴 제목은 한 줄 유지 + ... 말줄임 (truncate가 줄어들도록 min-w-0) -->
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
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useAuthStore } from '@/stores/auth'
import type { Post } from '@/types/community'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const posts = ref<Post[]>([])
const isLoading = ref(false)

async function fetchPosts() {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/v1/community/posts/')
    // 백엔드는 평탄한 snake_case로 내려준다 → camelCase로 정리
    posts.value = data.map((p: any) => ({
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
