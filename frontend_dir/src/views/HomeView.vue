<template>
  <main class="min-h-screen bg-slate-50 text-slate-900">
    <LandingHero />
    <LandingHowItWorks />
    <LandingFeatures />
    <LandingWhyMoa />
  </main>
</template>

<script setup lang="ts">
import LandingFeatures from '@/components/Home/LandingFeatures.vue'
import LandingHero from '@/components/Home/LandingHero.vue'
import LandingHowItWorks from '@/components/Home/LandingHowItWorks.vue'
import LandingWhyMoa from '@/components/Home/LandingWhyMoa.vue'
</script>
