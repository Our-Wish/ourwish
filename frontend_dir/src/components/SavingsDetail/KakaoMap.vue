<template>
  <div ref="mapRef" class="h-[360px] w-full overflow-hidden rounded-2xl"></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'

const mapRef = ref<HTMLDivElement | null>(null)

declare global {
  interface Window {
    kakao: any
  }
}

const loadKakaoMapScript = () => {
  return new Promise<void>((resolve, reject) => {
    if (window.kakao?.maps) {
      resolve()
      return
    }

    const existingScript = document.getElementById('kakao-map-script')
    if (existingScript) {
      existingScript.addEventListener('load', () => resolve())
      return
    }

    const script = document.createElement('script')
    script.id = 'kakao-map-script'
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&autoload=false`
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('카카오맵 SDK 로드 실패'))

    document.head.appendChild(script)
  })
}

onMounted(async () => {
  await loadKakaoMapScript()

  window.kakao.maps.load(() => {
    if (!mapRef.value) return

    const center = new window.kakao.maps.LatLng(37.5665, 126.978)

    const map = new window.kakao.maps.Map(mapRef.value, {
      center,
      level: 3,
    })

    new window.kakao.maps.Marker({
      position: center,
      map,
    })
  })
})
</script>
