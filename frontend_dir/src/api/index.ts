import axios from 'axios'
import type { AxiosInstance } from 'axios'

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

    if (error?.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true // 무한 루프 방지

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
          alert('다시 로그인이 필요합니다.')
          setAuthToken(null)
        }
      } else {
        alert('다시 로그인이 필요합니다.')
        setAuthToken(null)
      }
    }

    return Promise.reject(error)
  },
)

export default api
