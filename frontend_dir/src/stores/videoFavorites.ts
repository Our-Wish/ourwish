import { defineStore } from 'pinia'
import api from '@/api/index'

// 백엔드 GET /api/v1/favorites/videos/ 응답 한 건의 모양 (snake_case 그대로 받는다)
export interface VideoFavorite {
  video_id: string
  title: string
  thumbnail_url: string
  channel_name: string
  created_at: string
}

export const useVideoFavoritesStore = defineStore('videoFavorites', {
  state: () => ({
    favorites: [] as VideoFavorite[],
    isLoading: false,
  }),
  actions: {
    // 마이페이지 '찜한 영상' 탭을 열 때마다 최신 목록을 받아온다.
    async fetchVideoFavorites() {
      this.isLoading = true
      try {
        const { data } = await api.get('/api/v1/favorites/videos/')
        this.favorites = data
      } finally {
        this.isLoading = false
      }
    },
    // 영상 찜 등록. 백엔드는 get_or_create라 이미 찜했으면 기존 것을 그대로 돌려준다.
    async addVideoFavorite(payload: Omit<VideoFavorite, 'created_at'>) {
      const { data } = await api.post('/api/v1/favorites/videos/', payload)
      // 중복 push 방지 — 이미 목록에 있으면 그대로 둔다.
      if (!this.favorites.some((f) => f.video_id === data.video_id)) {
        this.favorites.unshift(data)
      }
    },
    // 서버에서 먼저 지운 뒤(성공해야) 로컬 목록에서도 제거한다.
    async removeVideoFavorite(videoId: string) {
      await api.delete(`/api/v1/favorites/videos/${videoId}/`)
      this.favorites = this.favorites.filter((f) => f.video_id !== videoId)
    },
    // 특정 영상이 현재 찜 목록에 있는지 (상세페이지 하트 상태 판단용)
    isFavorited(videoId: string): boolean {
      return this.favorites.some((f) => f.video_id === videoId)
    },
  },
})
