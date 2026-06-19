<template>
  <section
    class="relative -mt-16 flex min-h-180 w-full items-center justify-center overflow-hidden bg-linear-to-br from-slate-50 via-[#e4eef8] to-[#cfe0f2]"
  >
    <!-- 배경 글로우 -->
    <div
      class="pointer-events-none absolute top-0 left-1/3 h-96 w-96 rounded-full bg-sky-300/25 blur-3xl"
    />
    <div
      class="pointer-events-none absolute bottom-0 right-1/3 h-80 w-80 rounded-full bg-blue-300/20 blur-3xl"
    />

    <!-- 배경 장식 이미지 (2개) -->
    <img
      :src="mainImg"
      aria-hidden="true"
      class="pointer-events-none absolute -top-16 -left-20 w-208 rotate-[-18deg] opacity-60 drop-shadow-2xl"
    />
    <img
      :src="mainImg"
      aria-hidden="true"
      class="pointer-events-none absolute -bottom-16 -right-20 w-3xl rotate-15 opacity-55 drop-shadow-2xl"
    />

    <div class="relative z-10 flex flex-col items-center px-8 text-center">
      <h1 class="text-[9rem] font-semibold leading-none tracking-tighter text-slate-950">
        OUR WISH
      </h1>
      <p class="mt-3 text-3xl font-medium text-slate-800">
        쉽고, 간단하게, 나에게 맞는 적금을 찾다
      </p>

      <div class="mt-12 flex gap-4">
        <button
          @click="goToMyPage"
          class="rounded-2xl bg-slate-800/85 px-12 py-4 text-base font-semibold text-white backdrop-blur-sm transition hover:bg-slate-800 active:scale-95"
        >
          MY PAGE
        </button>
        <button
          @click="onStart"
          class="rounded-2xl bg-slate-800/85 px-12 py-4 text-base font-semibold text-white backdrop-blur-sm transition hover:bg-slate-800 active:scale-95"
        >
          적금 추천받으러 가기
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import mainImg from '@/assets/mainImg.png'
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

const goToMyPage = () => {
  if (isAuthenticated.value) {
    router.push({ name: 'mypage' })
  } else {
    authStore.openLoginModal()
  }
}
</script>

<style scoped></style>
