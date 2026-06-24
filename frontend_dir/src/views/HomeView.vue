<template>
  <main class="min-h-screen text-slate-900">
    <MobileLanding class="md:hidden" />
    <div class="hidden md:block">
      <LandingHero />
      <LandingFeatures />
    </div>
  </main>
</template>

<script setup lang="ts">
import LandingFeatures from '@/components/Home/LandingFeatures.vue'
import LandingHero from '@/components/Home/LandingHero.vue'
import MobileLanding from '@/components/Home/MobileLanding.vue'
</script>
