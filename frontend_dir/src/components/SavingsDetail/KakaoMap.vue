<template>
  <div>
    <div class="relative">
      <div ref="mapRef" class="h-45 w-full overflow-hidden rounded-xl"></div>
      <button
        v-if="!isLocating"
        @click="recenter"
        class="absolute bottom-2 right-2 z-10 rounded-full bg-white px-2.5 py-1 text-xs text-slate-600 shadow"
      >
        내 위치로
      </button>
    </div>

    <div v-if="isLocating" class="py-3 text-center text-sm text-slate-400">
      위치를 불러오는 중...
    </div>

    <template v-else>
      <p class="mt-2 text-xs leading-relaxed text-slate-400">
        📍 현재 위치를 기준으로 가까운 영업점을 안내해 드리고 있어요.<br />
        Wi-Fi 환경이나 기기 설정에 따라 위치에 다소 오차가 발생할 수 있습니다.
      </p>
      <div v-if="places.length" class="mt-3 divide-y divide-slate-100">
        <a
          v-for="place in visiblePlaces"
          :key="place.id"
          :href="`https://map.kakao.com/link/map/${place.place_name},${place.y},${place.x}`"
          target="_blank"
          rel="noopener noreferrer"
          class="block py-2.5 hover:opacity-70"
        >
          <p class="font-medium ml-1 text-slate-800">{{ place.place_name }}</p>
          <p class="text-sm ml-1 text-slate-500">{{ place.address_name }}</p>
        </a>
      </div>
      <p v-else class="mt-3 text-sm text-slate-400">근처 영업점 정보를 불러올 수 없어요.</p>

      <button
        @click="showModal = true"
        class="mt-2 w-full py-1 text-sm text-blue-500 hover:cursor-pointer hover:text-blue-300"
      >
        더 많은 영업점 보기
      </button>
    </template>

    <BranchMapModal v-if="showModal" :bank-name="bankName" @close="showModal = false" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import BranchMapModal from '@/components/SavingsDetail/BranchMapModal.vue'

const props = defineProps<{ bankName: string }>()

const mapRef = ref<HTMLDivElement | null>(null)
const isLocating = ref(true)
const places = ref<any[]>([])
const showModal = ref(false)
const mapInstance = ref<any>(null)
const userCenter = ref<any>(null)

const visiblePlaces = computed(() => places.value.slice(0, 3))

declare global {
  interface Window {
    kakao: any
  }
}

function recenter() {
  if (mapInstance.value && userCenter.value) {
    mapInstance.value.setCenter(userCenter.value)
  }
}

const loadKakaoMapScript = () => {
  return new Promise<void>((resolve, reject) => {
    if (window.kakao?.maps?.services) {
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
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${import.meta.env.VITE_KAKAO_MAP_KEY}&autoload=false&libraries=services`
    script.async = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('카카오맵 SDK 로드 실패'))

    document.head.appendChild(script)
  })
}

const getUserLocation = (): Promise<GeolocationCoordinates> => {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error('Geolocation not supported'))
      return
    }
    navigator.geolocation.getCurrentPosition((pos) => resolve(pos.coords), reject, {
      timeout: 8000,
    })
  })
}

onMounted(async () => {
  await loadKakaoMapScript()

  let lat = 37.5665
  let lng = 126.978

  try {
    const coords = await getUserLocation()
    lat = coords.latitude
    lng = coords.longitude
  } catch {
    // 위치 권한 거부 시 서울 중심 fallback
  }

  isLocating.value = false

  window.kakao.maps.load(() => {
    if (!mapRef.value) return

    const center = new window.kakao.maps.LatLng(lat, lng)
    userCenter.value = center

    const map = new window.kakao.maps.Map(mapRef.value, {
      center,
      level: 4,
    })
    mapInstance.value = map

    // 현재 위치 파란 점
    new window.kakao.maps.CustomOverlay({
      position: center,
      content:
        '<div style="width:14px;height:14px;background:#3b82f6;border:2.5px solid white;border-radius:50%;box-shadow:0 0 0 2px #3b82f6;"></div>',
      zIndex: 10,
      map,
    })

    const ps = new window.kakao.maps.services.Places()
    ps.keywordSearch(
      props.bankName,
      (data: any[], status: string) => {
        if (status !== window.kakao.maps.services.Status.OK) return
        places.value = data.slice(0, 5)

        data.slice(0, 5).forEach((place) => {
          const pos = new window.kakao.maps.LatLng(Number(place.y), Number(place.x))
          new window.kakao.maps.Marker({ position: pos, map })
        })
      },
      {
        location: center,

        sort: window.kakao.maps.services.SortBy.DISTANCE,
      },
    )
  })
})
</script>
