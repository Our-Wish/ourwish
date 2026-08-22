<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <TheNavbar />
    <main class="pt-16">
      <RouterView />
    </main>
    <GlobalModals />
  </div>
</template>

<script setup lang="ts">
import TheNavbar from '@/components/TheNavbar.vue'
import GlobalModals from '@/components/GlobalModals.vue'
</script>
