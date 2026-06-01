import { defineStore } from 'pinia'
import api, { setAuthToken } from '@/api'

const STORAGE_KEY = 'auth_token'

export type AuthUser = {
  email: string
  username?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(STORAGE_KEY) as string | null,
    user: null as AuthUser | null,
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
    logout() {
      this.setToken(null)
      this.user = null
    },
    async login(email: string, password: string) {
      const response = await api.post('/auth/login/', { email, password })
      const token = response.data.access || response.data.token || response.data.access_token
      if (token) {
        this.setToken(token)
        this.user = response.data.user ?? { email }
      }
      return response
    },
  },
})
