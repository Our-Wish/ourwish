<template>
  <div class="mx-auto max-w-md rounded-lg border bg-white p-8 shadow-sm">
    <h1 class="mb-6 text-2xl font-semibold text-slate-900">Login</h1>

    <form @submit.prevent="onSubmit" class="space-y-4">
      <label class="block">
        <span class="mb-2 block text-sm font-medium text-slate-700">Email</span>
        <input
          v-model="email"
          type="email"
          class="w-full rounded border border-slate-300 px-3 py-2 focus:border-slate-500 focus:outline-none"
          required
        />
      </label>

      <label class="block">
        <span class="mb-2 block text-sm font-medium text-slate-700">Password</span>
        <input
          v-model="password"
          type="password"
          class="w-full rounded border border-slate-300 px-3 py-2 focus:border-slate-500 focus:outline-none"
          required
        />
      </label>

      <button
        type="submit"
        class="w-full rounded bg-slate-900 px-4 py-2 text-white hover:bg-slate-700"
        :disabled="loading"
      >
        {{ loading ? 'Logging in...' : 'Login' }}
      </button>

      <p v-if="errorMessage" class="text-sm text-red-600">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref('')
const authStore = useAuthStore()
const router = useRouter()

const onSubmit = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    await authStore.login(email.value, password.value)
    router.push({ name: 'home' })
  } catch (error) {
    errorMessage.value = 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
