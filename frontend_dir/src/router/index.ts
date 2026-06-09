import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import GoalSetupView from '@/views/GoalSetupView.vue'
import RecommendationView from '@/views/RecommendationView.vue'

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
    {
      path: '/recommendation',
      name: 'recommendation',
      component: RecommendationView,
    },
  ],
})

export default router
