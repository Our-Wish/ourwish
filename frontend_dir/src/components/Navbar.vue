<template>
  <nav class="px-6 py-6">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <RouterLink to="/" class="text-lg font-semibold text-slate-900">Our Wish</RouterLink>
      </div>

      <div class="flex items-center gap-3 text-lg text-slate-700">
        <button
          v-if="!isAuthenticated"
          class="hover:text-slate-900"
          @click="authStore.openLoginModal()"
        >
          로그인
        </button>
        <button v-if="isAuthenticated" class="hover:text-slate-900" @click="logout">
          로그아웃
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const logout = () => {
  authStore.logout()
}
</script>
