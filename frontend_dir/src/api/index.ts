import axios from 'axios'
import type { AxiosInstance } from 'axios'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

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

// 세션 만료 시: 스토어 상태(token/user)까지 비워 네비가 로그인 상태로 남지 않게 한 뒤,
// 보호 페이지에 있으면 메인으로 돌려보낸다
function forceLogout() {
  // Pinia 스토어를 통해 token/user/sessionStorage를 한 번에 정리한다
  useAuthStore().logout()
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

// 진행 중인 refresh 요청. 여러 API가 동시에 401을 맞아도 refresh는 1번만 부르고,
// 나머지 요청들은 같은 Promise를 기다렸다가 새 토큰을 나눠 쓴다.
let refreshPromise: Promise<string> | null = null

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
        // 내가 refresh를 새로 시작하는 쪽인지 기억해 둔다(실패 알림을 1번만 띄우기 위해)
        const isRefreshOwner = refreshPromise === null
        try {
          if (!refreshPromise) {
            refreshPromise = api
              .post('/api/v1/accounts/token/refresh/', { refresh: refreshToken })
              .then(({ data }) => data.access as string)
              .finally(() => {
                refreshPromise = null // 성공/실패와 무관하게 다음 refresh를 위해 초기화
              })
          }
          const access = await refreshPromise
          setAuthToken(access)
          originalRequest.headers['Authorization'] = `Bearer ${access}`
          return api(originalRequest)
        } catch {
          // refresh 실패 → 낡은 토큰 정리 후 메인으로 (알림은 시작한 요청만 1번)
          if (isRefreshOwner) alert('다시 로그인이 필요합니다.')
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
