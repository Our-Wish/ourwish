<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center px-4 py-8">
    <div class="absolute inset-0 bg-slate-950/40" @click="emit('close')" />
    <div
      class="relative w-full max-w-xl rounded-[2rem] bg-white p-6 sm:p-10 shadow-2xl shadow-slate-950/20 max-h-[90vh] overflow-y-auto"
    >
      <button
        @click="emit('close')"
        class="absolute right-5 top-5 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
        aria-label="Close signup modal"
      >
        ×
      </button>

      <div class="space-y-1">
        <h1 class="mt-3 text-4xl font-semibold text-slate-950">회원가입</h1>
      </div>

      <p class="mt-3 text-base text-slate-500">
        회원가입하고 맞춤 예·적금 플랜을 추천받아보세요 :)
      </p>

      <form @submit.prevent="onSubmit" class="mt-8 space-y-4">
        <div>
          <input
            v-model="form.login_id"
            type="text"
            placeholder="아이디"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <input
            v-model="form.password"
            type="password"
            placeholder="비밀번호"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <input
            v-model="form.passwordConfirm"
            type="password"
            placeholder="비밀번호 확인"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <input
            v-model="form.nickname"
            type="text"
            placeholder="닉네임"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <p v-if="errorMessage" class="text-base text-red-600">{{ errorMessage }}</p>

        <button
          type="submit"
          class="mt-1 w-full rounded-2xl bg-blue-600 py-3.5 text-base font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? '가입 중...' : '가입하기' }}
        </button>
      </form>

      <div class="mt-4 flex items-center justify-center gap-1 text-base text-slate-500">
        <span>이미 계정이 있으신가요?</span>
        <button
          @click="emit('openLogin')"
          class="font-semibold text-blue-600 transition hover:text-blue-500"
        >
          로그인
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { isAxiosError } from 'axios'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{ close: []; openLogin: [] }>()

const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  login_id: '',
  password: '',
  passwordConfirm: '',
  nickname: '',
})

const authStore = useAuthStore()

const onSubmit = async () => {
  errorMessage.value = ''
  if (form.password !== form.passwordConfirm) {
    errorMessage.value = '비밀번호가 일치하지 않습니다.'
    return
  }
  loading.value = true
  try {
    await authStore.signup(form)
    emit('close')
  } catch (err) {
    // axios 에러일 때만 응답 본문을 보고, 백엔드 필드 에러(login_id)를 확인한다
    const data = isAxiosError<{ login_id?: string[] }>(err) ? err.response?.data : undefined
    if (data?.login_id) {
      errorMessage.value = '이미 사용 중인 아이디입니다.'
    } else {
      errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
    }
  } finally {
    loading.value = false
  }
}
</script>
