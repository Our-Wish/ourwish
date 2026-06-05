<template>
  <section class="border-t border-slate-200">
    <div class="mx-auto max-w-6xl px-6">
      <div class="max-w-2xl">
        <p class="text-sm uppercase tracking-[0.35em] text-blue-600">How it works</p>
        <h2 class="mt-4 text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
          3분이면 나에게 맞는 적금이<br />
          자동으로 나와요
        </h2>
        <p class="mt-6 text-lg leading-8 text-slate-600">
          기간, 금액, 매달 낼 수 있는 한도만 입력하면, 모아가 가장 쉬운 적금 경로를 찾아드립니다.
        </p>
      </div>

      <div class="mt-10 space-y-4">
        <div
          v-for="step in steps"
          :key="step.id"
          class="flex items-center justify-between rounded-3xl border border-slate-200 bg-slate-50 p-6 shadow-sm"
        >
          <div>
            <div
              class="mb-2 inline-flex h-10 w-10 items-center justify-center rounded-full bg-blue-50 text-blue-600"
            >
              {{ step.id }}
            </div>
            <p class="text-lg font-semibold text-slate-950">{{ step.title }}</p>
            <p class="mt-2 text-sm text-slate-600">{{ step.description }}</p>
          </div>
          <span class="text-2xl text-slate-300">→</span>
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
