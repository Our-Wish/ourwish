import { defineStore } from 'pinia'
import { setAuthToken } from '@/api'

const STORAGE_KEY = 'auth_token'

export type AuthUser = {
  email: string
  username?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(STORAGE_KEY) as string | null,
    user: null as AuthUser | null,
    showLoginModal: false,
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
    setToken(token: string | null) {
      this.token = token
      if (token) {
        localStorage.setItem(STORAGE_KEY, token)
      } else {
        localStorage.removeItem(STORAGE_KEY)
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
    logout() {
      this.setToken(null)
      this.user = null
    },
    async login(email: string, _password: string) {
      // TODO: 백엔드 연동 시 아래 mock 제거
      this.setToken('mock-token')
      this.user = { email }
    },
  },
})
