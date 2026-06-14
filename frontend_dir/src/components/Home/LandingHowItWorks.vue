<template>
  <section class="px-6 py-20">
    <div class="mx-auto max-w-6xl">
      <div class="mb-16 space-y-4 max-w-2xl">
        <span
          class="inline-block rounded-full bg-blue-100 px-4 py-1.5 text-sm font-semibold uppercase tracking-widest text-blue-700"
        >
          3단계
        </span>
        <h2 class="text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
          간단하게, 빠르게
        </h2>
        <p class="text-lg leading-relaxed text-slate-600">
          목표 금액과 조건만 입력하면 맞춤 적금 플랜을 추천해드려요.
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-3">
        <div
          v-for="step in steps"
          :key="step.id"
          class="group relative rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-50 to-slate-100/50 p-8 transition hover:border-blue-200 hover:shadow-lg hover:shadow-blue-100"
        >
          <div
            class="absolute -left-3 -top-3 inline-flex h-12 w-12 items-center justify-center rounded-full bg-blue-600 text-lg font-bold text-white shadow-lg"
          >
            {{ step.id }}
          </div>
          <div class="mt-6 space-y-3">
            <h3 class="text-xl font-bold text-slate-950">{{ step.title }}</h3>
            <p class="text-base leading-relaxed text-slate-600">{{ step.description }}</p>
          </div>
          <div
            class="mt-6 h-1 w-12 rounded-full bg-gradient-to-r from-blue-600 to-transparent transition group-hover:w-full"
          ></div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const steps = [
  {
    id: 1,
    title: '목표 설정하기',
    description: '모을 기간과 월 납입 금액을 입력하고 예상 수령액을 확인해보세요.',
  },
  {
    id: 2,
    title: '적금 플랜 비교하기',
    description: '상품별 금리와 예상 수령액을 비교하며 나에게 맞는 플랜을 찾아보세요.',
  },
  {
    id: 3,
    title: '가입하고 관리하기',
    description: '진행률과 만기 일정을 확인하며 목표까지 꾸준히 모아보세요.',
  },
]
</script>
