<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center px-4 py-8">
    <div class="absolute inset-0 bg-slate-950/40" @click="emit('close')" />
    <div
      class="relative w-full max-w-xl rounded-[2rem] bg-white p-10 shadow-2xl shadow-slate-950/20"
    >
      <button
        @click="emit('close')"
        class="absolute right-5 top-5 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
        aria-label="Close login modal"
      >
        ×
      </button>

      <div class="space-y-3">
        <p class="text-sm font-semibold uppercase tracking-[0.3em] text-slate-400">
          만나서 반가워요 👋🏻
        </p>
        <h1 class="text-3xl font-semibold text-slate-950">아이디와 비밀번호를 입력해주세요</h1>
      </div>

      <form @submit.prevent="onSubmit" class="mt-8 space-y-5">
        <div>
          <label class="mb-2 block text-sm font-medium text-slate-700">아이디</label>
          <input
            v-model="email"
            type="email"
            placeholder="아이디"
            class="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
            required
          />
        </div>

        <div>
          <label class="mb-2 block text-sm font-medium text-slate-700">비밀번호</label>
          <div class="relative">
            <input
              v-model="password"
              type="password"
              placeholder="비밀번호"
              class="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
              required
            />
          </div>
        </div>

        <button
          type="submit"
          class="w-full rounded-3xl bg-blue-600 px-5 py-3 text-base font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? '로그인 중...' : '로그인' }}
        </button>

        <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
      </form>

      <div class="mt-6 flex items-center justify-center gap-3 text-m text-slate-500">
        <button class="transition hover:text-slate-900">회원가입</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{ close: [] }>()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const authStore = useAuthStore()

const onSubmit = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(email.value, password.value)
    emit('close')
  } catch {
    errorMessage.value = '로그인에 실패했습니다. 아이디와 비밀번호를 확인해 주세요.'
  } finally {
    loading.value = false
  }
}
</script>
