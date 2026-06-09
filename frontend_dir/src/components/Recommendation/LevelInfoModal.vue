<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0 bg-slate-950/40" @click="emit('close')" />
    <div class="relative w-full max-w-lg rounded-3xl bg-white px-6 pb-8 pt-6">
      <button
        @click="emit('close')"
        class="absolute right-5 top-5 text-slate-400 hover:text-slate-700"
      >
        ✕
      </button>

      <span class="rounded-full bg-slate-100 px-3 py-1 text-sm font-semibold text-slate-700">
        {{ level }}
      </span>

      <h2 class="mt-3 text-3xl font-extrabold text-slate-900">{{ title }}</h2>
      <p class="mt-1 text-sm text-slate-500">{{ description }}</p>

      <p class="mt-6 text-xs font-semibold text-slate-400">대표적인 우대조건 예시</p>
      <ul class="mt-3 space-y-2">
        <li
          v-for="item in conditions"
          :key="item"
          class="rounded-2xl bg-slate-50 px-4 py-3 text-sm font-medium text-slate-800"
        >
          • {{ item }}
        </li>
      </ul>

      <p class="mt-5 text-xs text-slate-400">
        ※ 은행·상품마다 우대조건이 다를 수 있어요. 상품 상세 페이지에서 정확한 조건을 확인하세요.
      </p>

      <!-- 닫기 버튼 -->
      <button
        @click="emit('close')"
        class="mt-6 w-full rounded-2xl bg-slate-100 py-4 text-base font-semibold text-slate-700 hover:bg-slate-200"
      >
        닫기
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  level: 'LOW' | 'MID' | 'HIGH'
  title: string
  description: string
  conditions: string[]
}>()

const emit = defineEmits<{ close: [] }>()
</script>
