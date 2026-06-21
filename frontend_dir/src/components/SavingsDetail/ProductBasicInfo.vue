<template>
  <div class="rounded-2xl bg-white p-6 shadow-sm">
    <p class="text-base font-bold text-slate-900">상품 기본 정보</p>
    <div class="mt-3 divide-y divide-slate-100">
      <div
        v-for="item in conditions"
        :key="item.label"
        class="flex items-center gap-3 py-2.5"
      >
        <div class="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg bg-blue-50">
          <svg
            class="h-3.5 w-3.5 text-blue-400"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="1.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path
              v-if="item.label === '가입 대상'"
              d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
            />
            <path
              v-else-if="item.label === '가입 방법'"
              d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 8.25h3m-3 3h3m-6 3h.008v.008H6.75V15z"
            />
            <path
              v-else-if="item.label === '월 납입 한도'"
              d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"
            />
            <path
              v-else-if="item.label === '만기후 이자율'"
              d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z"
            />
            <path
              v-else
              d="M11.25 11.25l.041-.02a.75.75 0 011.063.852l-.708 2.836a.75.75 0 001.063.853l.041-.021M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9-3.75h.008v.008H12V8.25z"
            />
          </svg>
        </div>
        <span class="w-24 shrink-0 text-sm font-medium text-blue-500">{{ item.label }}</span>
        <span class="text-sm text-slate-700">{{ item.value }}</span>
      </div>
    </div>
    <p class="mt-4 text-sm text-slate-400">※ 자세한 내용은 상품설명서 및 약관을 확인해주세요.</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  conditions: { label: string; value: string }[]
}>()
</script>
