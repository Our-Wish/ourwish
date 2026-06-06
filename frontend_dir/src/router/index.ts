import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import GoalSetupView from '@/views/GoalSetupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/GoalSetup',
      name: 'goalsetup',
      component: GoalSetupView,
    },
  ],
})

export default router
