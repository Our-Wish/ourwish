<template>
  <main class="min-h-screen bg-slate-50 text-slate-900">
    <section class="mx-auto max-w-6xl px-6 py-20">
      <div class="grid gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
        <div class="space-y-8">
          <div class="space-y-4">
            <p class="text-sm font-semibold uppercase tracking-[0.35em] text-blue-600">MOA</p>
            <h1 class="text-5xl font-extrabold tracking-tight text-slate-950 sm:text-6xl">
              은행은 많은데<br />
              <span class="text-blue-600">나한테 맞는 건</span><br />
              딱 하나잖아요
            </h1>
            <p class="max-w-xl text-lg leading-8 text-slate-600">
              목표만 알려주면 매달 얼마를 어디에 모을지, 모아가 한눈에 정리해드려요.
            </p>
          </div>

          <div class="grid gap-4 sm:grid-cols-2">
            <div
              class="rounded-[2rem] bg-slate-950 px-7 py-8 text-white shadow-xl shadow-slate-950/10"
            >
              <p class="text-sm uppercase tracking-[0.25em] text-slate-400">달성까지</p>
              <p class="mt-4 text-4xl font-bold">D-298</p>
            </div>
            <div class="rounded-[2rem] bg-amber-300 px-7 py-8 shadow-xl shadow-amber-300/25">
              <p class="text-sm uppercase tracking-[0.25em] text-slate-700">최고금리</p>
              <p class="mt-4 text-4xl font-bold text-slate-950">연 4.5%</p>
            </div>
          </div>

          <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
            <RouterLink
              to="/login"
              class="inline-flex items-center justify-center rounded-full bg-blue-600 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500"
            >
              시작하기
            </RouterLink>
            <div
              class="rounded-full border border-slate-300 bg-white px-5 py-3 text-sm text-slate-700"
            >
              지금 바로 내 적금 맞춤 추천 받기
            </div>
          </div>
        </div>

        <div class="rounded-[2rem] bg-white p-8 shadow-[0_30px_80px_-30px_rgba(15,23,42,0.25)]">
          <div class="space-y-6">
            <div class="rounded-[2rem] bg-blue-600 p-8 text-white shadow-xl shadow-blue-600/20">
              <p class="text-sm uppercase tracking-[0.3em] text-blue-100">목표예산</p>
              <p class="mt-4 text-3xl font-semibold">25만원</p>
            </div>
            <div class="rounded-[2rem] bg-slate-950 p-6 text-white">
              <p class="text-sm uppercase tracking-[0.3em] text-slate-400">맞춤 제안</p>
              <p class="mt-4 text-xl font-semibold">내 상황에 딱 맞는 적금 플랜</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="border-t border-slate-200 bg-white py-16">
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

    <section class="bg-slate-50 py-16">
      <div class="mx-auto max-w-6xl px-6">
        <div class="max-w-2xl">
          <p class="text-sm uppercase tracking-[0.35em] text-blue-600">Features</p>
          <h2 class="mt-4 text-4xl font-extrabold tracking-tight text-slate-950 sm:text-5xl">
            사회초년생에게 꼭 필요한 것만
          </h2>
          <p class="mt-4 text-lg leading-8 text-slate-600">
            어려운 금융 용어 대신 한 줄 설명. 가입할 때 필요한 정보와 매달 얼마를 어떻게 모아야
            하는지를 한 화면에 보여드려요.
          </p>
        </div>

        <div class="mt-10 grid gap-4 md:grid-cols-2">
          <div class="rounded-[2rem] bg-slate-100 p-8">
            <div class="mb-4 text-3xl">📘</div>
            <p class="text-lg font-semibold text-slate-950">쉬운 약관</p>
            <p class="mt-2 text-sm text-slate-600">한 줄로 핵심만</p>
          </div>
          <div class="rounded-[2rem] bg-emerald-100 p-8">
            <div class="mb-4 text-3xl">🌱</div>
            <p class="text-lg font-semibold text-slate-950">난이도 표시</p>
            <p class="mt-2 text-sm text-slate-600">무리 안 가는 적금</p>
          </div>
          <div class="rounded-[2rem] bg-amber-100 p-8">
            <div class="mb-4 text-3xl">🗓️</div>
            <p class="text-lg font-semibold text-slate-950">D-Day 추적</p>
            <p class="mt-2 text-sm text-slate-600">목표까지 카운트다운</p>
          </div>
          <div class="rounded-[2rem] bg-purple-100 p-8">
            <div class="mb-4 text-3xl">🎒</div>
            <p class="text-lg font-semibold text-slate-950">준비물 안내</p>
            <p class="mt-2 text-sm text-slate-600">뭘 챙겨갈지 미리</p>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-slate-950 py-16 text-white">
      <div class="mx-auto max-w-6xl px-6">
        <div class="grid gap-10 lg:grid-cols-[1.2fr_0.8fr] lg:items-center">
          <div>
            <p class="text-sm uppercase tracking-[0.35em] text-blue-400">Why MOA</p>
            <h2 class="mt-4 text-4xl font-extrabold tracking-tight sm:text-5xl">
              약관은 짧게,<br />
              모으는 재미는 길게
            </h2>
            <p class="mt-4 max-w-xl text-lg leading-8 text-slate-300">
              어려운 금융 용어 대신 한 줄 설명. 가입할 때 뭔가 필요한지, 매달 얼마나 어떻게 모아야
              하는지 한 화면에서 다 보여드립니다.
            </p>
          </div>

          <div class="rounded-[2rem] bg-slate-900 p-8 shadow-2xl shadow-black/20">
            <div class="mb-6 flex flex-wrap gap-3">
              <span
                class="rounded-full bg-blue-600 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-white"
                >사회초년생</span
              >
              <span
                class="rounded-full bg-slate-700 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-slate-200"
                >23살 · 첫 적금</span
              >
            </div>
            <blockquote class="text-lg leading-8 text-slate-100">
              “약관 읽다가 포기했었는데, 모아는 한 줄로 알려줘서 진짜 내가 뭘 들었는지 알겠어요.”
            </blockquote>
            <p class="mt-6 text-sm text-slate-500">— 지원 (24, 디자이너)</p>
          </div>
        </div>
      </div>
    </section>
  </main>
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
