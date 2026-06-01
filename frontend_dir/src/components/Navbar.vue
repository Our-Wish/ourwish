<template>
  <nav class="border-b bg-white px-6 py-4 shadow-sm">
    <div class="mx-auto flex max-w-6xl items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <RouterLink to="/" class="font-semibold text-slate-900">OurWish</RouterLink>
      </div>

      <div class="flex items-center gap-3 text-sm text-slate-700">
        <RouterLink to="/" class="hover:text-slate-900">Home</RouterLink>
        <RouterLink v-if="!isAuthenticated" to="/login" class="hover:text-slate-900">Login</RouterLink>
        <button
          v-if="isAuthenticated"
          class="rounded border border-slate-300 px-3 py-1 text-slate-700 hover:bg-slate-50"
          @click="logout"
        >
          Logout
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
