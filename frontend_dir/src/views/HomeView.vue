<template>
  <div class="space-y-4 rounded-lg border border-slate-200 bg-white p-8 shadow-sm">
    <h1 class="text-3xl font-semibold text-slate-900">Home</h1>
    <p class="text-slate-600">OurWish 프론트엔드가 정상적으로 설정되었습니다.</p>

    <div v-if="isAuthenticated" class="rounded-lg bg-slate-50 p-4 text-slate-800">
      <p class="font-medium">로그인 완료</p>
      <p>이메일: {{ userEmail }}</p>
    </div>

    <div v-else class="rounded-lg bg-amber-50 p-4 text-amber-900">
      <p>로그인이 필요합니다. 상단 메뉴에서 Login을 눌러주세요.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const userEmail = computed(() => authStore.user?.email ?? 'Unknown')
</script>
