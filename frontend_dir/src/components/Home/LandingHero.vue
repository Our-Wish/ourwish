<template>
  <section class="mx-auto max-w-6xl px-6 py-20">
    <div class="grid gap-12 lg:grid-cols-[1.05fr_0.95fr] lg:items-center">
      <div class="space-y-8">
        <div class="space-y-4">
          <p class="text-sm font-semibold uppercase tracking-[0.35em] text-blue-600">OurWish</p>
          <h1 class="text-5xl font-extrabold tracking-tight text-slate-950 sm:text-6xl">
            은행은 많은데<br />
            <span class="text-blue-600">나한테 맞는 건</span><br />
            딱 하나잖아요
          </h1>
          <p class="max-w-xl text-lg leading-8 text-slate-600">
            목표만 알려주면 매달 얼마를 어디에 모을지, 모아가 한눈에 정리해드려요.
          </p>
        </div>

        <div class="flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            @click="authStore.openLoginModal()"
            class="flex w-full items-center justify-center rounded-full bg-blue-600 px-30 py-4 text-lg font-semibold text-white shadow-lg shadow-blue-600/20 transition hover:bg-blue-500 sm:w-auto"
          >
            시작하기
          </button>
        </div>
      </div>

      <div class="grid gap-4 sm:grid-cols-2">
        <div class="rounded-[2rem] bg-slate-950 px-7 py-8 text-white shadow-xl shadow-slate-950/10">
          <p class="text-sm uppercase tracking-[0.25em] text-slate-400">달성까지</p>
          <p class="mt-4 text-4xl font-bold">D-298</p>
        </div>
        <div class="rounded-[2rem] bg-amber-300 px-7 py-8 shadow-xl shadow-amber-300/25">
          <p class="text-sm uppercase tracking-[0.25em] text-slate-700">최고금리</p>
          <p class="mt-4 text-4xl font-bold text-slate-950">연 4.5%</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const { isAuthenticated } = storeToRefs(authStore)
</script>
