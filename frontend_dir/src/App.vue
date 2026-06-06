<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <Navbar />
    <main class="mx-auto max-w-6xl px-4 py-8">
      <RouterView />
    </main>
    <LoginModal v-if="authStore.showLoginModal" @close="authStore.closeLoginModal" />
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import LoginModal from '@/components/LoginModal.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
