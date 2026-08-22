<template>
  <!-- 본문이 너무 넓으면 제목이 안 잘리므로, 커뮤니티처럼 읽기 좋은 폭으로 제한한다 -->
  <div class="max-w-4xl">
    <h1 class="text-2xl font-extrabold text-slate-900 md:text-4xl">작성한 글</h1>
    <p class="mt-3 text-base font-light text-slate-400">
      커뮤니티에 남긴 내 글을 한곳에서 모아보세요.
    </p>

    <!-- 로딩 -->
    <div v-if="isLoading" class="mt-16 text-center text-base text-slate-400">불러오는 중...</div>

    <!-- 빈 상태 -->
    <div v-else-if="myPosts.length === 0" class="mt-20 text-center text-base text-slate-300">
      아직 작성한 글이 없어요.
    </div>

    <!-- 내 글 목록 -->
    <div v-else class="mt-8 space-y-4">
      <div
        v-for="post in myPosts"
        :key="post.id"
        class="group cursor-pointer rounded-2xl bg-white p-5 ring-1 ring-slate-200 transition hover:-translate-y-0.5 hover:ring-blue-200"
        @click="goDetail(post.id)"
      >
        <div class="flex items-center gap-2">
          <span
            class="min-w-0 flex-1 truncate text-lg font-bold text-slate-900 group-hover:text-blue-600"
          >
            {{ post.title }}
          </span>
          <span v-if="post.commentCount > 0" class="shrink-0 text-sm font-medium text-blue-400">
            [{{ post.commentCount }}]
          </span>
          <span class="shrink-0 text-sm text-slate-400">{{ post.createdAt }}</span>
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
import type { Post, PostApi } from '@/types/community'

const router = useRouter()
const authStore = useAuthStore()

const posts = ref<Post[]>([])
const isLoading = ref(false)

// 전체 글 중 내가 쓴 글만 — 별도 '내 글' 엔드포인트가 없어 author_id로 거른다.
const myPosts = computed(() => {
  const myId = authStore.user?.id
  if (myId == null) return []
  return posts.value.filter((p) => p.authorId === myId)
})

async function fetchPosts() {
  isLoading.value = true
  try {
    const { data } = await api.get('/api/v1/community/posts/')
    // 백엔드는 평탄한 snake_case → camelCase로 정리 (CommunityView와 동일)
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

function goDetail(postId: number) {
  router.push(`/community/${postId}`)
}

onMounted(fetchPosts)
</script>
