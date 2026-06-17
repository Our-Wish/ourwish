import { defineStore } from 'pinia'
import api, { setAuthToken } from '@/api'

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
    user: null as AuthUser | null,
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
    },
    async login(login_id: string, password: string) {
      const { data } = await api.post('/api/v1/accounts/login/', { login_id, password })
      this.setToken(data.access, data.refresh)
      this.user = data.member
    },
    async signup(payload: {
      login_id: string
      password: string
      nickname: string
      birth_date: string
      job_status: string
      marital_status: string
    }) {
      const { data } = await api.post('/api/v1/accounts/signup/', payload)
      this.setToken(data.access, data.refresh)
      this.user = data.member
    },
  },
})
