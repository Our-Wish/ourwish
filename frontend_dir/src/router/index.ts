import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import GoalSetupView from '@/views/GoalSetupView.vue'
import RecommendationView from '@/views/RecommendationView.vue'
import SavingsDetailView from '@/views/SavingsDetailView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior: () => ({ top: 0 }),
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
    {
      path: '/savings/:id',
      name: 'savings-detail',
      component: SavingsDetailView,
    },
  ],
})

export default router
