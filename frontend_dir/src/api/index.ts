import axios from 'axios'
import type { AxiosInstance } from 'axios'
import router from '@/router'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? '',
  headers: {
    'Content-Type': 'application/json',
  },
})

function getToken(): string | null {
  try {
    return sessionStorage.getItem('auth_token')
  } catch {
    return null
  }
}

const initialToken = getToken()
if (initialToken) {
  api.defaults.headers.common['Authorization'] = `Bearer ${initialToken}`
}

// 세션 만료 시: 토큰 정리 후, 보호 페이지에 있으면 메인으로 돌려보낸다
function forceLogout() {
  setAuthToken(null)
  sessionStorage.removeItem('refresh_token')
  if (router.currentRoute.value.meta.public !== true) {
    router.replace('/')
  }
}

export function setAuthToken(token: string | null) {
  if (token) {
    sessionStorage.setItem('auth_token', token)
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`
  } else {
    sessionStorage.removeItem('auth_token')
    delete api.defaults.headers.common['Authorization']
  }
}

api.interceptors.request.use((config) => {
  const token = getToken()
  if (token && config.headers) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const originalRequest = error.config
    // refresh 요청 자체가 401이면 다시 refresh하지 않는다(무한 루프 차단)
    const isRefreshCall = originalRequest?.url?.includes('/accounts/token/refresh/')

    if (error?.response?.status === 401 && !originalRequest._retry && !isRefreshCall) {
      originalRequest._retry = true // 같은 요청 1회만 재시도

      const refreshToken = sessionStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const { data } = await api.post('/api/v1/accounts/token/refresh/', {
            refresh: refreshToken,
          })
          setAuthToken(data.access)
          originalRequest.headers['Authorization'] = `Bearer ${data.access}`
          return api(originalRequest)
        } catch {
          // refresh 실패 → 낡은 토큰 정리 후 메인으로
          alert('다시 로그인이 필요합니다.')
          forceLogout()
        }
      } else {
        forceLogout()
      }
    }

    return Promise.reject(error)
  },
)

export default api
