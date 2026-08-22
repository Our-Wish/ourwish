<template>
  <div class="min-h-screen bg-linear-to-b from-slate-50 via-[#e4eef8] to-[#cfe0f2]">
    <section class="flex flex-col items-center px-7 pt-14 pb-10 text-center">
      <h1
        class="bg-gradient-to-r from-[#111827] via-[#123A73] to-[#023b90] bg-clip-text text-5xl font-bold tracking-[-0.06em] text-transparent"
      >
        OURWISH
      </h1>

      <p class="mt-4 text-base font-light leading-7 text-slate-600">
        쉽고, 간단하게, 나에게 맞는 예·적금을 찾다
      </p>

      <img :src="wonderWish" alt="아워위시 캐릭터" class="mt-12 w-40 drop-shadow-xl" />

      <div class="mt-10 flex w-full max-w-xs flex-col gap-3">
        <RouterLink
          to="/depositgoalsetup"
          class="rounded-2xl bg-slate-900 px-10 py-4 text-center text-base font-semibold text-white opacity-75 shadow-lg shadow-slate-900/20 transition hover:bg-slate-800 active:scale-95"
        >
          예금 추천받기
        </RouterLink>
        <RouterLink
          to="/goalsetup"
          class="rounded-2xl bg-slate-900 px-10 py-4 text-center text-base font-semibold text-white opacity-75 shadow-lg shadow-slate-900/20 transition hover:bg-slate-800 active:scale-95"
        >
          적금 추천받기
        </RouterLink>
      </div>
    </section>

    <section class="px-7 pt-10 pb-12 text-center">
      <h2 class="text-2xl font-bold leading-snug tracking-[-0.03em] text-slate-900">
        예·적금 찾기부터 관리까지<br />
        OURWISH에서 한 번에
      </h2>

      <p class="mt-4 text-sm font-normal leading-7 text-slate-500">
        조건 입력, 상품 추천, 금리 비교,<br />
        가입 상품 관리까지 쉽게 확인해보세요.
      </p>
    </section>

    <section class="px-7 pb-20">
      <div class="mx-auto flex max-w-sm flex-col gap-10">
        <article v-for="feature in features" :key="feature.label" class="flex items-start gap-5">
          <img :src="feature.img" :alt="feature.title" class="mt-1 w-16 shrink-0 drop-shadow-md" />

          <div>
            <p class="text-xs font-semibold tracking-[0.12em]" :class="feature.labelColor">
              {{ feature.label }}
            </p>

            <h3 class="mt-2 text-lg font-bold leading-snug tracking-[-0.02em] text-slate-900">
              {{ feature.title }}
            </h3>

            <p
              class="mt-2 text-xs font-normal leading-6 text-slate-500"
              v-html="feature.shortDesc"
            />
          </div>
        </article>
      </div>
    </section>
    <section
      class="relative flex min-h-[460px] items-center justify-center overflow-hidden px-7 py-20 text-center"
    >
      <img
        :src="wishFamily"
        alt="wishFamily"
        class="pointer-events-none absolute left-1/2 top-1/2 w-[360px] -translate-x-1/2 -translate-y-[60%] select-none opacity-20 drop-shadow-xl"
      />

      <div class="relative z-10">
        <h2 class="text-xl font-semibold leading-snug tracking-[-0.03em] text-slate-900">
          복잡한 금융을 더 쉽게 —<br />여러분의 Wish를 이루는 그날까지<br />
          OURWISH가 함께할게요.
        </h2>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import wonderWish from '@/assets/img/wishes/wonderWish.png'
import hiWish from '@/assets/img/wishes/hiWish.png'
import memoWish from '@/assets/img/wishes/memoWish.png'
import fightingWish from '@/assets/img/wishes/fightingWish.png'
import achieveWish from '@/assets/img/wishes/achieveWish.png'
import happyWish from '@/assets/img/wishes/happyWish.png'
import wishFamily from '@/assets/img/wishes/wishFamily.png'

const features = [
  {
    label: 'START',
    title: '몇 가지만 입력해보세요',
    shortDesc: '상품 유형과 기간, 금액을 입력하고 <br/> 내게 맞는 우대조건을 체크해보세요.',
    img: hiWish,
    labelColor: 'text-emerald-500',
  },
  {
    label: 'MATCH',
    title: '맞는 상품만 골라줘요',
    shortDesc: '나이, 금액, 우대조건을 고려해 <br/> 내 조건에 맞는 예·적금 상품을 보여줘요.',
    img: memoWish,
    labelColor: 'text-blue-500',
  },
  {
    label: 'COMPARE',
    title: '금리와 수령액까지 비교해요',
    shortDesc: '기본금리와 최고금리, 예상 수령액을 <br/>비교하면서 상품을 고를 수 있어요.',
    img: achieveWish,
    labelColor: 'text-indigo-500',
  },
  {
    label: 'EXPLAIN',
    title: '어려운 조건도 쉽게 확인해요',
    shortDesc: '복잡한 우대조건이나 낯선 금융 용어도<br/>더 쉬운 말로 확인할 수 있어요.',
    img: fightingWish,
    labelColor: 'text-purple-500',
  },
  {
    label: 'MANAGE',
    title: '가입한 상품을 모아봐요',
    shortDesc: '가입한 상품, 찜한 상품, 작성한 글을 <br/>한곳에 모아 관리할 수 있어요.',
    img: wonderWish,
    labelColor: 'text-amber-500',
  },
  {
    label: 'LOUNGE',
    title: '금융 정보도 둘러봐요',
    shortDesc: '영상, 커뮤니티, 금·은 시세까지 <br/>필요한 정보를 가볍게 확인해보세요.',
    img: happyWish,
    labelColor: 'text-pink-500',
  },
]
</script>
