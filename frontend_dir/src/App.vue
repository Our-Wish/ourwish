<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <Navbar />
    <main class="pt-16">
      <RouterView />
    </main>
    <GlobalModals />
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
import GlobalModals from '@/components/GlobalModals.vue'
</script>
