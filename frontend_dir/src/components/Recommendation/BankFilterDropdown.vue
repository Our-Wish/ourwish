<template>
  <div class="relative">
    <button
      @click="isOpen = !isOpen"
      class="flex items-center gap-2 whitespace-nowrap rounded-xl border px-5 py-2.5 text-base font-medium transition"
      :class="
        modelValue.length > 0
          ? 'border-indigo-400 bg-indigo-50 text-indigo-700'
          : 'border-slate-200 bg-white text-slate-700 hover:border-slate-300'
      "
    >
      <span>금융권 선택</span>
      <span
        v-if="modelValue.length > 0"
        class="rounded-full bg-indigo-500 px-1.5 text-xs text-white"
      >
        {{ modelValue.length }}
      </span>
    </button>

    <div v-if="isOpen" class="fixed inset-0 z-10" @click="isOpen = false" />
    <div
      v-if="isOpen"
      class="absolute right-0 top-full z-20 mt-2 w-80 rounded-2xl bg-white p-4 shadow-xl ring-1 ring-slate-100"
    >
      <p class="mb-2 text-xs font-semibold text-slate-400">금융권</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="filter in tierFilters"
          :key="filter.key"
          @click="select(filter.key)"
          class="rounded-full px-4 py-1.5 text-sm font-medium transition"
          :class="isActive(filter.key) ? 'bg-indigo-500 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
        >
          {{ filter.label }}
        </button>
      </div>

      <p class="mb-2 mt-4 text-xs font-semibold text-slate-400">은행</p>
      <div class="flex flex-wrap gap-2">
        <button
          v-for="filter in bankFilters"
          :key="filter.key"
          @click="select(filter.key)"
          class="rounded-full px-4 py-1.5 text-sm font-medium transition"
          :class="isActive(filter.key) ? 'bg-indigo-500 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'"
        >
          {{ filter.label }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ modelValue: string[] }>()
const emit = defineEmits<{ 'update:modelValue': [value: string[]] }>()

const isOpen = ref(false)

const tierFilters = [
  { key: 'all', label: '전체' },
  { key: 'first_tier', label: '제1금융권' },
  { key: 'savings', label: '저축은행' },
]

const bankFilters = [
  { key: '신한은행', label: '신한은행' },
  { key: '농협은행주식회사', label: '농협은행' },
  { key: '국민은행', label: '국민은행' },
  { key: '우리은행', label: '우리은행' },
  { key: '주식회사 하나은행', label: '하나은행' },
  { key: '주식회사 카카오뱅크', label: '카카오뱅크' },
  { key: '토스뱅크 주식회사', label: '토스뱅크' },
]

function isActive(key: string): boolean {
  if (key === 'all') return props.modelValue.length === 0
  return props.modelValue.includes(key)
}

function select(key: string) {
  if (key === 'all') {
    emit('update:modelValue', [])
    return
  }
  const next = [...props.modelValue]
  const idx = next.indexOf(key)
  if (idx === -1) next.push(key)
  else next.splice(idx, 1)
  emit('update:modelValue', next)
}
</script>
