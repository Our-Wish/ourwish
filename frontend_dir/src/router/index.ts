import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import GoalSetupView from '@/views/GoalSetupView.vue'
import RecommendationView from '@/views/RecommendationView.vue'
import SavingsDetailView from '@/views/SavingsDetailView.vue'
import MyPageView from '@/views/MyPageView.vue'
import CommunityView from '@/views/CommunityView.vue'
import CommunityPostDetailView from '@/views/CommunityPostDetailView.vue'
import CommunityWriteView from '@/views/CommunityWriteView.vue'
import GoldSilverView from '@/views/GoldSilverView.vue'
import VideoSearchView from '@/views/VideoSearchView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'
import DepositGoalSetupView from '@/views/DepositGoalSetupView.vue'
import DepositRecommendationView from '@/views/DepositRecommendationView.vue'

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
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView,
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView,
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
    },
    {
      path: '/goldsilver',
      name: 'goldsilver',
      component: GoldSilverView,
    },
    {
      path: '/videosearch',
      name: 'videosearch',
      component: VideoSearchView,
    },
    {
      path: '/videos/:videoId',
      name: 'video-detail',
      component: VideoDetailView,
      props: true,
    },
    {
      path: '/depositgoalsetup',
      name: 'depositgoalsetup',
      component: DepositGoalSetupView,
    },
    {
      path: '/depositrecommendation',
      name: 'depositrecommendation',
      component: DepositRecommendationView,
    },
  ],
})

export default router
