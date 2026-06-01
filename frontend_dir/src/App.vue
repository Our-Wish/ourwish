<template>
  <div class="min-h-screen bg-slate-50 text-slate-900">
    <Navbar />
    <main class="mx-auto max-w-6xl px-4 py-8">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import Navbar from '@/components/Navbar.vue'
</script>
