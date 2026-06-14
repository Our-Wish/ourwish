<template>
  <nav class="sticky top-0 z-50 border-b border-slate-100 px-6 backdrop-blur-md">
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between">
      <RouterLink to="/" class="text-xl font-bold tracking-tight text-slate-900"
        >OurWish</RouterLink
      >

      <div class="flex items-center gap-3">
        <template v-if="!isAuthenticated">
          <button
            class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100"
            @click="authStore.openLoginModal()"
          >
            로그인
          </button>
        </template>

        <template v-else>
          <div class="relative" ref="dropdownRef">
            <button
              class="flex h-9 w-9 items-center justify-center rounded-full bg-blue-600 text-sm font-bold text-white transition hover:bg-blue-500"
              @click="toggleDropdown"
            >
              {{ userInitial }}
            </button>

            <div
              v-if="isOpen"
              class="absolute right-0 mt-2 w-40 overflow-hidden rounded-2xl border border-slate-100 bg-white shadow-xl shadow-slate-200/60"
            >
              <RouterLink
                to="/mypage"
                class="flex items-center gap-2 px-4 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
                @click="isOpen = false"
              >
                마이페이지
              </RouterLink>
              <button
                class="flex w-full items-center gap-2 px-4 py-3 text-sm font-medium text-red-500 transition hover:bg-slate-50"
                @click="logout"
              >
                로그아웃
              </button>
            </div>
          </div>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)

const isOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)

const userInitial = computed(() => {
  return authStore.user?.email?.charAt(0).toUpperCase() ?? 'U'
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const logout = () => {
  authStore.logout()
  isOpen.value = false
}

const handleClickOutside = (e: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', handleClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', handleClickOutside))
</script>
