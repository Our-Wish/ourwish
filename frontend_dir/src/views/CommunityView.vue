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
          <!-- 로그인한 사용자만 글쓰기 가능 -->
          <button
            v-if="isAuthenticated"
            class="rounded-full bg-blue-500 px-5 py-2.5 text-base font-semibold text-white shadow-sm shadow-blue-200 transition hover:bg-blue-600 active:scale-95"
            @click="showWriteModal = true"
          >
            글쓰기 +
          </button>
        </div>
      </div>

      <!--
        [API] GET /api/v1/community/posts/
        - 연결 위치: onMounted에서 fetchPosts() 호출
        - 현재는 목업 데이터(posts) 사용 중
      -->
      <div class="overflow-hidden rounded-3xl bg-white shadow-sm ring-1 ring-slate-100">
        <table class="w-full">
          <thead>
            <tr class="border-b border-slate-100 bg-slate-50/60">
              <th class="w-14 py-3.5 pl-6 pr-4 text-left text-sm font-semibold text-slate-400">번호</th>
              <th class="py-3.5 pr-4 text-left text-sm font-semibold text-slate-400">제목</th>
              <th class="py-3.5 pr-4 text-left text-sm font-semibold text-slate-400">작성자</th>
              <th class="py-3.5 pr-6 text-right text-sm font-semibold text-slate-400">날짜</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="post in posts"
              :key="post.id"
              class="group cursor-pointer border-b border-slate-100 transition last:border-0 hover:bg-blue-50/40"
              @click="router.push(`/community/${post.id}`)"
            >
              <td class="py-4 pl-6 pr-4 text-base text-slate-300">{{ post.id }}</td>
              <td class="py-4 pr-4 text-base font-semibold text-slate-800 group-hover:text-blue-600">
                {{ post.title }}
              </td>
              <td class="py-4 pr-4 text-base text-slate-500">{{ post.authorNickname }}</td>
              <td class="py-4 pr-6 text-right text-sm text-slate-400">{{ post.createdAt }}</td>
            </tr>
          </tbody>
        </table>

        <div v-if="posts.length === 0" class="px-6 py-16 text-center text-base text-slate-400">
          아직 게시글이 없어요. 첫 번째 글을 작성해보세요!
        </div>
      </div>
    </div>
  </div>

  <!--
    [다음 단계] 글쓰기 모달 (Step 3에서 구현)
    <WritePostModal v-if="showWriteModal" @close="showWriteModal = false" @submit="onPostSubmit" />
  -->
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { Post } from '@/types/community'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

const showWriteModal = ref(false)

/*
  [API 연결 포인트]
  GET /api/v1/community/posts/

  async function fetchPosts() {
    const res = await api.get('/api/v1/community/posts/')
    posts.value = res.data.map((p: any) => ({
      id: p.id,
      title: p.title,
      content: p.content,
      authorNickname: p.author.nickname,
      createdAt: p.created_at.slice(0, 10),
      commentCount: p.comment_count,
    }))
  }
  onMounted(fetchPosts)
*/

// 목업 데이터 — API 연결 후 제거
const posts = ref<Post[]>([
  {
    id: 1,
    title: '예금 금리 어디가 제일 높나요?',
    content: '',
    authorNickname: '금융왕',
    createdAt: '2026-06-23',
    commentCount: 5,
  },
  {
    id: 2,
    title: '적금 vs 예금 뭐가 더 나을까요?',
    content: '',
    authorNickname: '초보투자자',
    createdAt: '2026-06-22',
    commentCount: 3,
  },
  {
    id: 3,
    title: '첫 적금 가입 성공! 후기 공유해요',
    content: '',
    authorNickname: '절약러',
    createdAt: '2026-06-21',
    commentCount: 8,
  },
  {
    id: 4,
    title: '금리 인상되면 예금이 유리한가요?',
    content: '',
    authorNickname: '뉴비',
    createdAt: '2026-06-20',
    commentCount: 2,
  },
])
</script>
