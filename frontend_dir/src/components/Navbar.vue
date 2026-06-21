<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 px-6 transition-colors duration-300',
      isHome ? 'bg-transparent' : 'bg-white border-b border-slate-100',
    ]"
  >
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold tracking-tight text-slate-900"
        >OURWISH</RouterLink
      >

      <div class="flex items-center gap-4">
        <template v-if="!isAuthenticated">
          <button
            class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
            @click="authStore.openLoginModal()"
          >
            로그인
          </button>
        </template>

        <template v-else>
          <RouterLink
            to="/mypage"
            class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
          >
            나의 적금 관리
          </RouterLink>
          <button
            class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
            @click="logout"
          >
            로그아웃
          </button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useRoute } from 'vue-router'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
const route = useRoute()
const isHome = computed(() => route.path === '/')

const logout = () => {
  authStore.logout()
}
</script>
