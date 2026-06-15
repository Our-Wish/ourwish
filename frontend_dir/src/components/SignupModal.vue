<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center px-4 py-8">
    <div class="absolute inset-0 bg-slate-950/40" @click="emit('close')" />
    <div
      class="relative w-full max-w-xl rounded-[2rem] bg-white p-10 shadow-2xl shadow-slate-950/20 max-h-[90vh] overflow-y-auto"
    >
      <button
        @click="emit('close')"
        class="absolute right-5 top-5 inline-flex h-10 w-10 items-center justify-center rounded-full text-slate-500 transition hover:bg-slate-100 hover:text-slate-900"
        aria-label="Close signup modal"
      >
        ×
      </button>

      <div class="space-y-1">
        <h1 class="text-4xl font-bold text-slate-950">회원가입</h1>
      </div>

      <p class="mt-3 text-base text-slate-500">나의 적금 플랜을 시작해보세요 ✨</p>

      <form @submit.prevent="onSubmit" class="mt-8 space-y-6">
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
            v-model="form.nickname"
            type="text"
            placeholder="닉네임"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label class="mb-1.5 block text-base font-medium text-slate-600">생년월일</label>
          <input
            v-model="form.birth_date"
            type="date"
            class="w-full rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3.5 text-base text-slate-900 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label class="mb-1.5 block text-base font-medium text-slate-600">직업</label>
          <div class="flex gap-2">
            <button
              v-for="opt in jobOptions"
              :key="opt.value"
              type="button"
              @click="form.job_status = opt.value"
              :class="[
                'rounded-full px-5 py-2.5 text-base font-medium transition',
                form.job_status === opt.value
                  ? 'bg-slate-900 text-white'
                  : 'border border-slate-200 bg-white text-slate-600 hover:border-slate-400',
              ]"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

        <div>
          <label class="mb-1.5 block text-base font-medium text-slate-600">결혼 여부</label>
          <div class="flex gap-2">
            <button
              v-for="opt in maritalOptions"
              :key="opt.value"
              type="button"
              @click="form.marital_status = opt.value"
              :class="[
                'rounded-full px-5 py-2.5 text-base font-medium transition',
                form.marital_status === opt.value
                  ? 'bg-slate-900 text-white'
                  : 'border border-slate-200 bg-white text-slate-600 hover:border-slate-400',
              ]"
            >
              {{ opt.label }}
            </button>
          </div>
        </div>

        <p v-if="errorMessage" class="text-base text-red-600">{{ errorMessage }}</p>

        <button
          type="submit"
          class="w-full rounded-2xl bg-blue-600 px-5 py-3.5 text-base font-semibold text-white transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-60"
          :disabled="loading"
        >
          {{ loading ? '가입 중...' : '가입하기' }}
        </button>
      </form>

      <div class="mt-6 flex items-center justify-center gap-1 text-base text-slate-500">
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

const emit = defineEmits<{ close: []; openLogin: [] }>()

const jobOptions = [
  { value: 'STUDENT', label: '학생' },
  { value: 'EMPLOYED', label: '직장인' },
  { value: 'OTHER', label: '기타' },
]

const maritalOptions = [
  { value: 'SINGLE', label: '미혼' },
  { value: 'MARRIED', label: '기혼' },
]

const loading = ref(false)
const errorMessage = ref('')

const form = reactive({
  login_id: '',
  password: '',
  nickname: '',
  birth_date: '',
  job_status: '',
  marital_status: '',
})

const onSubmit = async () => {
  loading.value = true
  errorMessage.value = ''
  try {
    // TODO: API 연결
    console.log('signup form:', form)
  } catch {
    errorMessage.value = '회원가입에 실패했습니다. 다시 시도해주세요.'
  } finally {
    loading.value = false
  }
}
</script>
