<template>
  <section class="px-6 py-20">
    <div class="mx-auto max-w-6xl">
      <div class="mb-16 space-y-4 max-w-2xl">
        <span
          class="inline-block rounded-full bg-blue-100 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-blue-700"
        >
          기능
        </span>
        <h2 class="text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
          당신의 목표를 위한 적금 플래너
        </h2>
        <p class="text-lg leading-relaxed text-slate-600">
          목표 설정부터 상품 비교, 진행 관리까지 한 곳에서 해결하세요.
        </p>
      </div>

      <div class="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <div
          v-for="feature in features"
          :key="feature.title"
          class="group rounded-3xl border border-slate-200 bg-white p-6 transition hover:shadow-lg"
          :class="[feature.hoverBorder, feature.hoverShadow]"
        >
          <div
            class="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-xl text-xl"
            :class="feature.iconBg"
          >
            {{ feature.icon }}
          </div>
          <h3 class="font-semibold text-slate-950">{{ feature.title }}</h3>
          <p class="mt-2 text-sm text-slate-600 whitespace-pre-line">{{ feature.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const features = [
  {
    icon: '🔎',
    title: '예상 수령액 계산',
    description: '내 조건으로 얼마까지 모을 수 있는지\n미리 확인해보세요.',
    iconBg: 'bg-blue-100',
    hoverBorder: 'hover:border-blue-300',
    hoverShadow: 'hover:shadow-blue-100',
  },
  {
    icon: '🌱',
    title: 'AI 상품 해설',
    description: '금리, 우대조건, 약관까지\n쉽게 풀어서 설명해드려요.',
    iconBg: 'bg-emerald-100',
    hoverBorder: 'hover:border-emerald-300',
    hoverShadow: 'hover:shadow-emerald-100',
  },
  {
    icon: '🏦',
    title: '맞춤 상품 추천',
    description: '조건에 맞는 적금 상품을 비교하고\n나에게 맞는 플랜을 찾아보세요.',
    iconBg: 'bg-amber-100',
    hoverBorder: 'hover:border-amber-300',
    hoverShadow: 'hover:shadow-amber-100',
  },
  {
    icon: '🎯',
    title: '목표 달성 관리',
    description: '진행률과 만기 일정을 확인하며\n목표까지 꾸준히 모아보세요!',
    iconBg: 'bg-purple-100',
    hoverBorder: 'hover:border-purple-300',
    hoverShadow: 'hover:shadow-purple-100',
  },
]
</script>
