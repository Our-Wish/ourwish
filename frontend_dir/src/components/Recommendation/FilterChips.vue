<template>
  <div>
    <div class="flex gap-2">
      <button
        v-for="filter in filters"
        :key="filter.key"
        @click="emit('update:modelValue', filter.key)"
        class="rounded-full px-4 py-2 text-sm font-medium transition"
        :class="
          modelValue === filter.key
            ? 'bg-slate-900 text-white'
            : 'bg-white border border-slate-200 text-slate-600 hover:border-slate-400'
        "
      >
        {{ filter.label }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { type FilterKey } from '@/constants/levelInfo'

defineProps<{ modelValue: FilterKey }>()
const emit = defineEmits<{ 'update:modelValue': [value: FilterKey] }>()

const filters = [
  { key: 'BASE' as FilterKey, label: '기본금리만' },
  { key: 'LOW' as FilterKey, label: '쉬운 조건까지' },
  { key: 'MID' as FilterKey, label: '보통 조건까지' },
  { key: 'HIGH' as FilterKey, label: '모든 조건까지' },
]
</script>
