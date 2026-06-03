<template>
  <nav class="border-b bg-white px-6 py-4 shadow-sm">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <RouterLink to="/" class="font-semibold text-slate-900">Our Wish</RouterLink>
      </div>

      <div class="flex items-center gap-3 text-sm text-slate-700">
        <RouterLink v-if="!isAuthenticated" to="/login" class="hover:text-slate-900"
          >로그인</RouterLink
        >
        <button
          v-if="isAuthenticated"
          class="rounded border border-slate-300 px-3 py-1 text-slate-700 hover:bg-slate-50"
          @click="logout"
        >
          로그아웃
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push({ name: 'home' })
}
</script>
