<template>
  <div class="min-h-screen bg-linear-to-b from-[#F7F9FB] to-[#DFEAF7]">
    <div class="flex px-32 pb-12 pt-8">
      <aside class="flex w-1/5 flex-col pr-8">
        <div>
          <p class="pl-3 text-lg font-bold text-slate-800">금융 라운지</p>
          <nav class="mt-3 space-y-1 pl-3">
            <button
              @click="activeMenu = 'video'"
              class="w-full cursor-pointer rounded-xl px-3 py-2.5 text-left text-base font-semibold transition"
              :class="activeMenu === 'video' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'"
            >
              금융TV
            </button>
            <button
              @click="activeMenu = 'goldsilver'"
              class="w-full cursor-pointer rounded-xl px-3 py-2.5 text-left text-base font-semibold transition"
              :class="activeMenu === 'goldsilver' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'"
            >
              금/은 시세
            </button>
            <button
              @click="activeMenu = 'community'"
              class="w-full cursor-pointer rounded-xl px-3 py-2.5 text-left text-base font-semibold transition"
              :class="activeMenu === 'community' ? 'text-blue-600' : 'text-slate-700 hover:bg-slate-100'"
            >
              커뮤니티
            </button>
          </nav>
        </div>
      </aside>

      <div class="w-px bg-slate-200" />

      <main class="flex-1 px-14 pt-2">
        <VideoSection v-if="activeMenu === 'video'" />
        <GoldSilverSection v-if="activeMenu === 'goldsilver'" />
        <CommunitySection v-if="activeMenu === 'community'" />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import VideoSection from '@/components/FinanceLounge/VideoSection.vue'
import GoldSilverSection from '@/components/FinanceLounge/GoldSilverSection.vue'
import CommunitySection from '@/components/FinanceLounge/CommunitySection.vue'

const activeMenu = ref<'video' | 'goldsilver' | 'community'>('video')
</script>
