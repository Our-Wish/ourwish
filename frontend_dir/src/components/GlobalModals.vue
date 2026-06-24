<template>
  <LoginModal v-if="authStore.showLoginModal" @close="authStore.closeLoginModal" />
  <SignupModal
    v-if="authStore.showSignupModal"
    @close="authStore.closeSignupModal"
    @open-login="() => { authStore.closeSignupModal(); authStore.openLoginModal() }"
  />
</template>

<script setup lang="ts">
import LoginModal from '@/components/LoginModal.vue'
import SignupModal from '@/components/SignupModal.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>
