<template>
  <section class="px-6 py-20">
    <div class="mx-auto max-w-6xl">
      <div class="mb-16 space-y-4 max-w-2xl">
        <span
          class="inline-block rounded-full bg-blue-100 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-blue-700"
        >
          3단계
        </span>
        <h2 class="text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
          간단하고 빠르게
        </h2>
        <p class="text-lg leading-relaxed text-slate-600">
          당신의 조건을 입력하면 맞춤형 상품을 자동으로 제시합니다.
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
            <p class="text-sm leading-relaxed text-slate-600">{{ step.description }}</p>
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
    title: '목표 정하기',
    description: '기간, 금액, 매달 낼 수 있는 한도만 알려주세요',
  },
  {
    id: 2,
    title: '맞춤 추천 받기',
    description: '조건에 맞는 적금·예금을 한 번에 비교',
  },
  {
    id: 3,
    title: '가입하고 모으기',
    description: '진행률을 보면서 D-Day까지 차곡차곡',
  },
]
</script>
