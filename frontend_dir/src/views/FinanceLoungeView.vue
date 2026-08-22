<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div class="flex flex-col px-5 pb-12 pt-6 lg:flex-row lg:px-32 lg:pt-8">
      <aside class="flex flex-col lg:w-1/5 lg:pr-8">
        <div>
          <nav class="mt-1 flex gap-1 overflow-x-auto pb-1 lg:mt-3 lg:block lg:space-y-1 lg:overflow-visible lg:pb-0 lg:pl-8">
            <button
              @click="activeMenu = 'video'"
              class="shrink-0 whitespace-nowrap cursor-pointer rounded-xl px-3 py-2.5 text-left text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'video' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              금융TV
            </button>
            <button
              @click="activeMenu = 'goldsilver'"
              class="shrink-0 whitespace-nowrap cursor-pointer rounded-xl px-3 py-2.5 text-left text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'goldsilver' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              금/은 시세
            </button>
            <button
              @click="activeMenu = 'community'"
              class="shrink-0 whitespace-nowrap cursor-pointer rounded-xl px-3 py-2.5 text-left text-sm md:text-base lg:w-full font-semibold transition"
              :class="
                activeMenu === 'community' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'
              "
            >
              커뮤니티
            </button>
          </nav>
        </div>
        <div class="mt-40 hidden text-center lg:block">
          <img :src="heartWish" alt="위시" class="mx-auto w-40" />
          <p class="mt-4 text-sm text-slate-400 break-keep">오늘의 금융 인사이트를 만나보세요 💡</p>
        </div>
      </aside>

      <div class="hidden w-px bg-slate-200 lg:block" />

      <main class="mt-5 flex-1 lg:mt-0 lg:px-14 lg:pt-2">
        <VideoSection v-if="activeMenu === 'video'" />
        <GoldSilverSection v-if="activeMenu === 'goldsilver'" />
        <CommunitySection v-if="activeMenu === 'community'" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import VideoSection from '@/components/FinanceLounge/VideoSection.vue'
import GoldSilverSection from '@/components/FinanceLounge/GoldSilverSection.vue'
import CommunitySection from '@/components/FinanceLounge/CommunitySection.vue'
import heartWish from '@/assets/img/wishes/heartWish.png'

type Menu = 'video' | 'goldsilver' | 'community'
const route = useRoute()
const validTabs: Menu[] = ['video', 'goldsilver', 'community']
const getTabFromQuery = () => {
  const q = route.query.tab as string
  return validTabs.includes(q as Menu) ? (q as Menu) : 'video'
}
const activeMenu = ref<Menu>(getTabFromQuery())

watch(() => route.query.tab, () => {
  activeMenu.value = getTabFromQuery()
})
</script>
