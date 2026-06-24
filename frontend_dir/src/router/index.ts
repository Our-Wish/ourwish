import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import GoalSetupView from '@/views/GoalSetupView.vue'
import RecommendationView from '@/views/RecommendationView.vue'
import SavingsDetailView from '@/views/SavingsDetailView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CommunityPostDetailView from '@/views/CommunityPostDetailView.vue'
import CommunityWriteView from '@/views/CommunityWriteView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'
import DepositGoalSetupView from '@/views/DepositGoalSetupView.vue'
import DepositRecommendationView from '@/views/DepositRecommendationView.vue'
import FinanceLoungeView from '@/views/FinanceLoungeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior: () => ({ top: 0 }),
  routes: [
    {
      // 메인(랜딩)만 비로그인 허용
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { public: true },
    },
    {
      path: '/GoalSetup',
      name: 'goalsetup',
      component: GoalSetupView,
      meta: { public: true },
    },
    {
      path: '/recommendation',
      name: 'recommendation',
      component: RecommendationView,
      meta: { public: true },
    },
    {
      path: '/savings/:id',
      name: 'savings-detail',
      component: SavingsDetailView,
      meta: { public: true },
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
    },
    {
      // 글쓰기 — :id보다 먼저 둬서 'write'가 상세로 잡히지 않게 한다
      path: '/community/write',
      name: 'community-write',
      component: CommunityWriteView,
    },
    {
      // 글 수정 — 같은 컴포넌트를 props.id로 작성/수정 겸용
      path: '/community/:id/edit',
      name: 'community-edit',
      component: CommunityWriteView,
      props: true,
    },
    {
      path: '/community/:id',
      name: 'community-post-detail',
      component: CommunityPostDetailView,
      props: true,
      meta: { public: true },
    },
    {
      path: '/videos/:videoId',
      name: 'video-detail',
      component: VideoDetailView,
      props: true,
      meta: { public: true },
    },
    {
      path: '/depositgoalsetup',
      name: 'depositgoalsetup',
      component: DepositGoalSetupView,
      meta: { public: true },
    },
    {
      path: '/depositrecommendation',
      name: 'depositrecommendation',
      component: DepositRecommendationView,
      meta: { public: true },
    },
    {
      path: '/financelounge',
      name: 'financelounge',
      component: FinanceLoungeView,
      meta: { public: true },
    },
  ],
})

// 전역 가드: public이 아닌 페이지는 로그인 필수
router.beforeEach((to) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isAuthenticated) {
    authStore.openLoginModal()
    return { name: 'home' }
  }
})

export default router
