<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 px-6 transition-colors duration-300',
      isHome ? 'bg-transparent' : 'bg-[#F7F9FB]',
    ]"
  >
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold tracking-tight text-slate-900"
        >OURWISH</RouterLink
      >

      <div class="flex items-center gap-4">
        <RouterLink
          to="/videosearch"
          class="rounded-full px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100"
        >
          금융TV
        </RouterLink>
        <RouterLink
          to="/goldsilver"
          class="rounded-full px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100"
        >
          금/은 시세
        </RouterLink>
        <RouterLink
          to="/community"
          class="rounded-full px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100"
        >
          커뮤니티
        </RouterLink>
        <RouterLink
          to="/depositgoalsetup"
          class="rounded-full px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100"
        >
          예금 추천받기
        </RouterLink>
        <RouterLink
          to="/goalsetup"
          class="rounded-full px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100"
        >
          적금 추천받기
        </RouterLink>
        <RouterLink
          to="/mypage"
          class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
        >
          마이페이지
        </RouterLink>

        <button
          v-if="!isAuthenticated"
          class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
          @click="authStore.openLoginModal()"
        >
          로그인
        </button>
        <button
          v-else
          class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
          @click="logout"
        >
          로그아웃
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
const route = useRoute()
const router = useRouter()
const isHome = computed(() => route.path === '/')

const logout = () => {
  authStore.logout()
  // 보호 페이지에 머무르지 않도록 메인으로 이동
  router.push('/')
}
</script>
