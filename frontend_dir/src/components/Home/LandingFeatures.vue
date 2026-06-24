<template>
  <div class="bg-linear-to-b from-[#ddecfc] via-[#e4eff9] to-white">
    <div class="mx-auto max-w-5xl px-8 pt-32 pb-20 text-center">
      <h2 class="text-5xl font-extrabold leading-tight tracking-tight text-slate-900 sm:text-6xl">
        예·적금 찾기부터 관리까지<br />
        아워위시가 쉽게 도와드려요
      </h2>

      <p class="mt-8 text-xl leading-relaxed text-slate-500">
        조건 입력, 상품 추천, 금리 비교, AI 설명, 가입 상품 관리까지<br />
        복잡한 금융 생활을 한곳에서 한눈에 확인해보세요.
      </p>
    </div>

    <div
      v-for="(feature, i) in features"
      :key="feature.label"
      :ref="(el) => observe(el, i)"
      class="mx-auto max-w-5xl px-8 py-24 flex items-center gap-16 transition-all duration-700 ease-out"
      :class="[
        i % 2 === 0 ? 'flex-row' : 'flex-row-reverse',
        visible.has(i) ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10',
      ]"
    >
      <div class="flex-1 min-w-0">
        <span class="text-sm font-bold uppercase tracking-[0.3em]" :class="feature.labelColor">
          {{ feature.label }}
        </span>
        <h3
          class="mt-4 text-4xl font-extrabold text-slate-900 leading-tight sm:text-5xl whitespace-pre-line"
        >
          {{ feature.title }}
        </h3>
        <p class="mt-6 text-lg text-slate-500 leading-relaxed max-w-md whitespace-pre-line">
          {{ feature.description }}
        </p>
      </div>
      <div class="shrink-0 w-72 flex items-center justify-center">
        <img :src="feature.img" :alt="feature.title" class="w-full drop-shadow-xl mr-10" />
      </div>
    </div>

    <div
      :ref="(el) => observe(el, features.length)"
      class="mx-auto max-w-4xl px-8 pt-16 pb-32 flex flex-col items-center text-center transition-all duration-700 ease-out"
      :class="
        visible.has(features.length) ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'
      "
    >
      <img :src="wishFamily" alt="아워위시" class="w-96 drop-shadow-xl" />
      <p class="mt-12 text-4xl font-extrabold text-slate-900 leading-snug sm:text-5xl">
        복잡한 금융을 더 쉽고 간편하게<br />
        여러분의 Wish가 이루어지는 순간까지<br />
        아워위시가 함께할게요.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import hiWish from '@/assets/img/wishes/hiWish.png'
import fightingWish from '@/assets/img/wishes/fightingWish.png'
import wonderWish from '@/assets/img/wishes/wonderWish.png'
import memoWish from '@/assets/img/wishes/memoWish.png'
import achieveWish from '@/assets/img/wishes/achieveWish.png'
import happyWish from '@/assets/img/wishes/happyWish.png'
import wishFamily from '@/assets/img/wishes/wishFamily.png'

const features = [
  {
    label: 'START',
    title: '몇 가지 조건만 입력해보세요.',
    description:
      '상품 유형과 기간, 금액을 입력하고\n내게 적용될 수 있는 우대조건을 체크해보세요.\n아워위시가 내 조건에 맞는 예·적금 상품과\n 예상 수령액을 함께 보여드려요.   ',
    img: hiWish,
    labelColor: 'text-emerald-500',
  },
  {
    label: 'MATCH',
    title: '맞는 상품만 골라줘요',
    description:
      '나이, 가입 금액, 기간, 우대조건까지 고려해\n내 조건에 맞는 상품만 추천해줘요.\n은행별로 직접 찾아보지 않아도 괜찮아요.',
    img: achieveWish,
    labelColor: 'text-blue-500',
  },
  {
    label: 'COMPARE',
    title: '금리와 수령액까지 비교해요',
    description:
      '기본금리와 최고금리뿐 아니라 세후 예상 수령액까지\n한눈에 비교할 수 있어요.\n상품 상세 정보와 가입 조건도 함께 확인해요.',
    img: wonderWish,
    labelColor: 'text-indigo-500',
  },
  {
    label: 'EXPLAIN',
    title: '어려운 설명은\nAI가 쉽게 풀어줘요',
    description:
      '복잡한 우대조건과 낯선 금융 용어도 AI가 쉬운 말로 정리해줘요.\n궁금한 점은 챗봇에게 바로 물어볼 수 있어요.',
    img: fightingWish,
    labelColor: 'text-purple-500',
  },
  {
    label: 'MANAGE',
    title: '가입한 상품을\n한눈에 관리해요',
    description:
      '가입한 예·적금 상품부터 찜한 상품, 작성한 글까지\n마이페이지에서 한 번에 확인할 수 있어요.\n목표 달성률과 금리 비교도 함께 보여줘요.',
    img: fightingWish,
    labelColor: 'text-amber-500',
  },
  {
    label: 'LOUNGE',
    title: '금융 정보도\n함께 둘러봐요',
    description:
      '금융라운지에서 영상, 커뮤니티, 금융 시세까지\n한 번에 확인할 수 있어요.\n혼자 고민하지 않아도 괜찮아요.',
    img: happyWish,
    labelColor: 'text-pink-500',
  },
]

const visible = ref<Set<number>>(new Set())

const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const idx = Number((entry.target as HTMLElement).dataset.idx)
        visible.value = new Set([...visible.value, idx])
        io.unobserve(entry.target)
      }
    })
  },
  { threshold: 0.15 },
)

function observe(el: unknown, idx: number) {
  if (el instanceof HTMLElement) {
    el.dataset.idx = String(idx)
    io.observe(el)
  }
}

onUnmounted(() => io.disconnect())
</script>
