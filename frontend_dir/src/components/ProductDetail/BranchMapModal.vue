<template>
  <div
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
    @click.self="$emit('close')"
  >
    <div
      class="relative mx-4 flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl bg-white"
    >
      <div class="flex items-center justify-between border-b px-6 py-4">
        <p class="text-lg font-bold text-slate-900">영업점 찾기</p>
        <button @click="$emit('close')" class="text-slate-400 hover:text-slate-600">✕</button>
      </div>

      <div class="flex gap-2 border-b px-6 py-4">
        <select
          v-model="selectedCity"
          @change="selectedDistrict = ''"
          class="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700"
        >
          <option value="">광역시/도 선택</option>
          <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
        </select>
        <select
          v-model="selectedDistrict"
          :disabled="!selectedCity"
          class="flex-1 rounded-lg border border-slate-200 px-3 py-2 text-sm text-slate-700 disabled:opacity-40"
        >
          <option value="">시/군/구 선택</option>
          <option v-for="d in currentDistricts" :key="d" :value="d">{{ d }}</option>
        </select>
        <button
          @click="search"
          :disabled="!selectedCity"
          class="rounded-lg bg-blue-500 px-4 py-2 text-sm font-medium text-white disabled:opacity-40"
        >
          검색
        </button>
      </div>

      <div ref="modalMapRef" class="h-64 w-full flex-shrink-0"></div>

      <div class="flex-1 overflow-y-auto divide-y divide-slate-100 px-6">
        <p v-if="!results.length" class="py-6 text-center text-sm text-slate-400">
          지역을 선택하고 검색하세요.
        </p>
        <a
          v-for="place in results"
          :key="place.id"
          :href="`https://map.kakao.com/link/map/${place.place_name},${place.y},${place.x}`"
          target="_blank"
          rel="noopener noreferrer"
          class="block py-3 hover:opacity-70"
        >
          <p class="font-medium text-slate-800">{{ place.place_name }}</p>
          <p class="text-sm text-slate-500">{{ place.address_name }}</p>
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { KOREA_REGIONS } from '@/constants/koreaRegions'
import type { KakaoMap, KakaoMarker, KakaoPlace } from '@/types/kakao'

const props = defineProps<{ bankName: string }>()
defineEmits<{ close: [] }>()

const modalMapRef = ref<HTMLDivElement | null>(null)
const selectedCity = ref('')
const selectedDistrict = ref('')
const results = ref<KakaoPlace[]>([])
const modalMap = ref<KakaoMap | null>(null)
const markers = ref<KakaoMarker[]>([])

const cities = Object.keys(KOREA_REGIONS)
const currentDistricts = computed(() =>
  selectedCity.value ? KOREA_REGIONS[selectedCity.value] : [],
)

function clearMarkers() {
  markers.value.forEach((m) => m.setMap(null))
  markers.value = []
}

function search() {
  if (!selectedCity.value || !modalMap.value) return
  const keyword = `${selectedDistrict.value || selectedCity.value} ${props.bankName}`

  const ps = new window.kakao.maps.services.Places()
  ps.keywordSearch(keyword, (data: KakaoPlace[], status: string) => {
    clearMarkers()

    if (status !== window.kakao.maps.services.Status.OK) {
      results.value = []
      return
    }

    results.value = data

    // 콜백은 나중에 실행되므로, 함수 첫머리의 modalMap 체크가 여기까진 안 통한다.
    // 지역 변수로 다시 잡아 null 아님을 확정한 뒤 사용한다.
    const map = modalMap.value
    const first = data[0]
    if (map && first) {
      const center = new window.kakao.maps.LatLng(Number(first.y), Number(first.x))
      map.setCenter(center)
      map.setLevel(6)

      data.slice(0, 15).forEach((place) => {
        const pos = new window.kakao.maps.LatLng(Number(place.y), Number(place.x))
        const marker = new window.kakao.maps.Marker({ position: pos, map })
        markers.value.push(marker)
      })
    }
  })
}

onMounted(() => {
  window.kakao.maps.load(() => {
    if (!modalMapRef.value) return
    const center = new window.kakao.maps.LatLng(37.5665, 126.978)
    modalMap.value = new window.kakao.maps.Map(modalMapRef.value, {
      center,
      level: 8,
    })
  })
})
</script>
