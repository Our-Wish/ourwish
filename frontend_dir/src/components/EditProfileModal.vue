<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center px-4 py-8">
    <div class="absolute inset-0 bg-slate-950/40" @click="emit('close')" />
    <div
      class="relative w-full max-w-xl rounded-[2rem] bg-white p-10 shadow-2xl shadow-slate-950/20"
    >
      <button
        @click="emit('close')"
        class="absolute text-2xl cursor-pointer right-5 top-5 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition hover:font-semibold hover:text-slate-900"
        aria-label="닫기"
      >
        ×
      </button>

      <h1 class="text-2xl font-bold text-slate-950">프로필 수정</h1>
      <p class="mt-2 text-sm font-light text-slate-500">
        OURWISH에서 사용할 닉네임을 입력해주세요.
      </p>

      <form @submit.prevent="onSubmit" class="mt-8 space-y-4">
        <div>
          <input
            v-model="nickname"
            type="text"
            placeholder="새 닉네임을 입력해주세요."
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <p v-if="errorMessage" class="text-sm ml-2 text-red-500">{{ errorMessage }}</p>

        <button
          type="submit"
          class="w-full rounded-2xl bg-blue-600 px-5 py-3.5 text-base font-medium text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? '저장 중' : '변경사항 저장' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const emit = defineEmits<{ close: [] }>()

const authStore = useAuthStore()
const nickname = ref(authStore.user?.nickname ?? '')
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const onSubmit = async () => {
  if (!nickname.value.trim()) {
    errorMessage.value = '닉네임을 입력해 주세요.'
    return
  }

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const { data } = await api.patch('/api/v1/accounts/me/', { nickname: nickname.value.trim() })
    authStore.updateUser({ nickname: data.nickname })
    successMessage.value = '닉네임이 변경되었어요!'
    setTimeout(() => emit('close'), 1000)
  } catch {
    errorMessage.value = '변경에 실패했어요. 다시 시도해 주세요.'
  } finally {
    loading.value = false
  }
}
</script>
