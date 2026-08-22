import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue(), vueDevTools(), tailwindcss()],
  server: {
    open: '/',
    // 파일 감시가 막힌 샌드박스 환경(VITE_WATCH_POLL=1)에서만 폴링 감시 사용.
    // 일반 개발에서는 기존과 동일하게 OS 파일 이벤트를 쓴다.
    watch: process.env.VITE_WATCH_POLL ? { usePolling: true, interval: 300 } : undefined,
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
