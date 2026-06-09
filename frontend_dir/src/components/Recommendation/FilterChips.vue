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
    <p
      v-if="modelValue !== 'BASE'"
      @click="showLevelModal = true"
      class="mt-2 ml-3 cursor-pointer text-xs text-slate-400 hover:text-slate-600"
    >
      ⓘ {{ modelValue }} 레벨 알아보기
    </p>

    <LevelInfoModal
      v-if="showLevelModal"
      :level="modelValue"
      title="그냥 하면 됨"
      description="대부분 사람이 무리 없이 채울 수 있는 조건이에요"
      :conditions="['급여이체 (건당 50만원 이상)', '자사 앱 가입/로그인', '자동이체 1건 이상 등록']"
      @close="showLevelModal = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import LevelInfoModal from './LevelInfoModal.vue'

type FilterKey = 'BASE' | 'LOW' | 'MID' | 'HIGH'

defineProps<{ modelValue: FilterKey }>()
const emit = defineEmits<{ 'update:modelValue': [value: FilterKey] }>()

const showLevelModal = ref(false)

const filters = [
  { key: 'BASE' as FilterKey, label: '기본금리만' },
  { key: 'LOW' as FilterKey, label: 'LOW 우대까지' },
  { key: 'MID' as FilterKey, label: 'MID 우대까지' },
  { key: 'HIGH' as FilterKey, label: 'HIGH 우대까지' },
]
</script>
