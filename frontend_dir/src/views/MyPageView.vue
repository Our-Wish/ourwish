<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div class="flex flex-col px-5 pb-12 pt-6 lg:flex-row lg:px-32 lg:pt-8">
      <aside class="flex flex-col lg:w-1/5 lg:pr-8">
        <div>
          <nav class="mt-1 flex gap-1 overflow-x-auto pb-1 lg:mt-3 lg:block lg:space-y-1 lg:overflow-visible lg:pb-0 lg:pl-8">
            <button
              @click="activeMenu = 'products'"
              class="shrink-0 whitespace-nowrap text-left cursor-pointer px-3 py-2.5 rounded-xl text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'products' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              나의 금융상품
            </button>
            <button
              @click="activeMenu = 'marketRate'"
              class="shrink-0 whitespace-nowrap text-left cursor-pointer px-3 py-2.5 rounded-xl text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'marketRate' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              가입 상품 금리 비교
            </button>

            <button
              @click="activeMenu = 'wishlist'"
              class="shrink-0 whitespace-nowrap text-left cursor-pointer px-3 py-2.5 rounded-xl text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'wishlist' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              찜한 상품
            </button>

            <button
              @click="activeMenu = 'videos'"
              class="shrink-0 whitespace-nowrap text-left cursor-pointer px-3 py-2.5 rounded-xl text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'videos' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              찜한 영상
            </button>

            <button
              @click="activeMenu = 'posts'"
              class="shrink-0 whitespace-nowrap text-left cursor-pointer px-3 py-2.5 rounded-xl text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'posts' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              작성한 글
            </button>
          </nav>
        </div>

        <div class="mt-36 hidden text-center lg:block">
          <img :src="achieveWish" alt="위시" class="mx-auto w-44" />
          <p class="mt-3 text-sm text-slate-400 break-keep">오늘도 목표에 한 걸음 더!</p>
        </div>
      </aside>

      <div class="hidden w-px bg-slate-200 lg:block" />

      <main class="mt-5 flex-1 lg:mt-0 lg:px-14 lg:pt-2">
        <ProductsSection v-if="activeMenu === 'products'" />
        <WishlistSection v-if="activeMenu === 'wishlist'" />
        <VideosSection v-if="activeMenu === 'videos'" />
        <PostsSection v-if="activeMenu === 'posts'" />
        <MarketRate v-if="activeMenu === 'marketRate'" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import achieveWish from '@/assets/img/wishes/achieveWish.png'
import ProductsSection from '@/components/MyPage/ProductsSection.vue'
import WishlistSection from '@/components/MyPage/WishlistSection.vue'
import VideosSection from '@/components/MyPage/VideosSection.vue'
import PostsSection from '@/components/MyPage/PostsSection.vue'
import MarketRate from '@/components/MyPage/MarketRate.vue'

type Menu = 'products' | 'wishlist' | 'videos' | 'posts' | 'marketRate'
const route = useRoute()
const validTabs: Menu[] = ['products', 'wishlist', 'videos', 'posts', 'marketRate']
const getTabFromQuery = () => {
  const q = route.query.tab as string
  return validTabs.includes(q as Menu) ? (q as Menu) : 'products'
}
const activeMenu = ref<Menu>(getTabFromQuery())

watch(
  () => route.query.tab,
  () => {
    activeMenu.value = getTabFromQuery()
  },
)
</script>
