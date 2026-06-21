<template>
  <div class="rounded-2xl bg-white p-6 shadow-sm">
    <p class="text-base font-bold text-slate-900">가입 정보</p>
    <div class="mt-3 divide-y divide-slate-100">
      <div v-for="item in conditions" :key="item.label" class="flex items-start gap-3 py-2.5">
        <span class="w-24 shrink-0 text-sm font-medium text-blue-500">{{ item.label }}</span>
        <span class="whitespace-pre-line break-keep text-sm font-normal text-slate-700">{{
          item.value
        }}</span>
      </div>
    </div>
    <p class="mt-4 text-sm text-slate-400">※ 실제 가입 전 상품설명서와 약관을 꼭 확인해주세요.</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  conditions: { label: string; value: string }[]
}>()
</script>
