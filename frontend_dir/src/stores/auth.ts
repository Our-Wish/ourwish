import { defineStore } from 'pinia'
import api, { setAuthToken } from '@/api'
import { useEnrollmentStore } from '@/stores/enrollment'
import { useFavoritesStore } from '@/stores/favorites'
import { useVideoFavoritesStore } from '@/stores/videoFavorites'
import { useGoalStore } from '@/stores/goal'

const ACCESS_KEY = 'auth_token'
const REFRESH_KEY = 'refresh_token'

export type AuthUser = {
  id: number
  login_id: string
  nickname: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: sessionStorage.getItem(ACCESS_KEY) as string | null,
    user: JSON.parse(sessionStorage.getItem('auth_user') ?? 'null') as AuthUser | null,
    showLoginModal: false,
    showSignupModal: false,
  }),
  getters: {
    isAuthenticated: (state) => Boolean(state.token),
  },
  actions: {
    initialize() {
      if (this.token) {
        setAuthToken(this.token)
      }
    },
    setToken(token: string | null, refresh: string | null = null) {
      this.token = token
      if (token) {
        sessionStorage.setItem(ACCESS_KEY, token)
      } else {
        sessionStorage.removeItem(ACCESS_KEY)
      }
      if (refresh) {
        sessionStorage.setItem(REFRESH_KEY, refresh)
      } else {
        sessionStorage.removeItem(REFRESH_KEY)
      }
      setAuthToken(token)
    },
    setUser(user: AuthUser | null) {
      this.user = user
    },
    openLoginModal() {
      this.showLoginModal = true
    },
    closeLoginModal() {
      this.showLoginModal = false
    },
    openSignupModal() {
      this.showLoginModal = false
      this.showSignupModal = true
    },
    closeSignupModal() {
      this.showSignupModal = false
    },
    logout() {
      this.setToken(null, null)
      this.user = null
      sessionStorage.removeItem('auth_user')
      // 같은 탭에서 다른 계정으로 로그인해도 이전 계정의 상품·찜·플랜이 남지 않도록
      // 개인 데이터 스토어를 초기 상태로 되돌린다. ($reset = 옵션 스토어의 state() 초기값으로 복원)
      useEnrollmentStore().$reset()
      useFavoritesStore().$reset()
      useVideoFavoritesStore().$reset()
      useGoalStore().$reset()
    },
    async login(login_id: string, password: string) {
      const { data } = await api.post('/api/v1/accounts/login/', { login_id, password })
      this.setToken(data.access, data.refresh)
      this.user = data.member
      sessionStorage.setItem('auth_user', JSON.stringify(data.member))
    },
    updateUser(partial: Partial<AuthUser>) {
      if (!this.user) return
      this.user = { ...this.user, ...partial }
      sessionStorage.setItem('auth_user', JSON.stringify(this.user))
    },
    async signup(payload: { login_id: string; password: string; nickname: string }) {
      const { data } = await api.post('/api/v1/accounts/signup/', payload)
      this.setToken(data.access, data.refresh)
      this.user = data.member
      sessionStorage.setItem('auth_user', JSON.stringify(data.member))
    },
  },
})
