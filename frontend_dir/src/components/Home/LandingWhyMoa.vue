<template>
  <section class="px-6 py-20"">
    <div class="mx-auto max-w-6xl px-6">
      <div>
        <p class="text-sm uppercase tracking-[0.35em] text-blue-600">Why MOA</p>
        <h2 class="mt-4 text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
          약관은 짧게,<br />
          모으는 재미는 길게
        </h2>
        <p class="mt-4 text-lg leading-8 text-slate-600">
          어려운 금융 용어 대신 한 줄 설명. 가입할 때 뭐가 필요한지, 매달 얼마를 어떻게 모아야
          하는지 — 한 화면에서 다 보여드려요!
        </p>

        <div class="mt-8 rounded-[2rem] bg-gray-50 p-8 shadow-lg shadow-gray-200/50">
          <div class="mb-6 flex flex-wrap gap-3">
            <span
              class="rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-white"
              >사회초년생</span
            >
            <span
              class="rounded-full bg-gray-200 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-slate-700"
              >23살 · 첫 적금</span
            >
          </div>
          <blockquote class="text-lg leading-8 text-slate-900">
            "약관 읽다가 포기했었는데, Our Wish는 한 줄로 알려줘서 진짜 내가 어떤 상품에
            가입해야하는지 한 번에 알겠어요."
          </blockquote>
          <p class="mt-6 text-sm text-slate-600">김주우 (28, 개발자)</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
