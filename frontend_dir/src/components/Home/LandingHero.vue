<template>
  <section class="mx-auto max-w-6xl px-6 py-20">
    <div class="grid gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
      <div class="space-y-8">
        <div class="space-y-4">
          <p class="text-sm font-semibold uppercase tracking-[0.35em] text-blue-600">OurWish</p>
          <h1 class="text-5xl font-extrabold tracking-tight text-slate-950 sm:text-6xl">
            목표만 알려주면
            <br />
            <span class="text-blue-600">내게 맞는 적금,</span><br />
            한눈에 찾아드릴게요
          </h1>
          <p class="max-w-xl text-lg leading-8 text-slate-600">
            기간과 월 납입 금액을 입력하면 예상 수령액과 추천 상품을 정리해드려요.
          </p>
        </div>

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            @click="onStart"
            class="flex w-full items-center justify-center rounded-full bg-blue-600 px-30 py-4 text-lg font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 sm:w-auto"
          >
            내 적금 플랜 시작하기
          </button>
        </div>
      </div>

      <div class="flex flex-col gap-4">
        <div
          class="rounded-[2rem] bg-white px-7 py-6 shadow-xl shadow-slate-200/60 border border-slate-100"
        >
          <p class="text-sm font-semibold uppercase tracking-widest text-slate-400">입력</p>
          <div class="mt-4 flex gap-8">
            <div>
              <p class="text-sm text-slate-400">월 납입액</p>
              <p class="mt-1 text-3xl font-bold text-slate-950">20만원</p>
            </div>
            <div>
              <p class="text-sm text-slate-400">기간</p>
              <p class="mt-1 text-3xl font-bold text-slate-950">12개월</p>
            </div>
          </div>
        </div>

        <div class="rounded-[2rem] bg-slate-950 px-7 py-6 text-white shadow-xl shadow-slate-950/20">
          <p class="text-sm font-semibold uppercase tracking-widest text-slate-400">예상 수령액</p>
          <p class="mt-3 text-4xl font-bold">약 246만원</p>
          <p class="mt-1 text-sm text-slate-400">원금 240만원 + 이자 6만원</p>
          <p class="mt-4 text-sm text-slate-500">평균 금리 연 3.5%</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'

const authStore = useAuthStore()
const router = useRouter()
const { isAuthenticated } = storeToRefs(authStore)

const onStart = () => {
  if (isAuthenticated.value) {
    router.push({ name: 'goalsetup' })
  } else {
    authStore.openLoginModal()
  }
}
</script>
