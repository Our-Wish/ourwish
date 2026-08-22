// 카카오맵 JS SDK 타입 선언.
// 공식 타입 패키지가 없어서, 우리 코드가 실제로 쓰는 부분만 직접 선언한다.
// (런타임 코드가 아니라 "window.kakao가 이런 모양"이라는 타입 정보만 담는 파일)

// 좌표 한 점 (위도 lat, 경도 lng)
export interface KakaoLatLng {
  getLat(): number
  getLng(): number
}

// 지도 인스턴스 — setCenter(중심 이동)·setLevel(확대 수준)만 쓴다
export interface KakaoMap {
  setCenter(latlng: KakaoLatLng): void
  setLevel(level: number): void
}

// 마커 — setMap(null)로 지도에서 제거
export interface KakaoMarker {
  setMap(map: KakaoMap | null): void
}

// 키워드 검색 결과 한 건 (카카오 로컬 API 응답 필드명 그대로, 좌표는 문자열)
export interface KakaoPlace {
  id: string
  place_name: string
  address_name: string
  road_address_name: string
  phone: string
  x: string // 경도(longitude)
  y: string // 위도(latitude)
  distance: string // 중심 좌표까지 거리(m) — location 옵션을 줬을 때만
}

// window.kakao.maps 전체 모양
export interface KakaoMapsSdk {
  load(callback: () => void): void
  LatLng: new (lat: number, lng: number) => KakaoLatLng
  Map: new (container: HTMLElement, options: { center: KakaoLatLng; level: number }) => KakaoMap
  Marker: new (options: {
    position: KakaoLatLng
    map?: KakaoMap | null
    zIndex?: number
  }) => KakaoMarker
  CustomOverlay: new (options: {
    position: KakaoLatLng
    content: string
    zIndex?: number
    map?: KakaoMap | null
  }) => unknown
  services: {
    Places: new () => {
      keywordSearch(
        keyword: string,
        callback: (data: KakaoPlace[], status: string) => void,
        options?: { location?: KakaoLatLng; sort?: string },
      ): void
    }
    Status: { OK: string; ZERO_RESULT: string; ERROR: string }
    SortBy: { DISTANCE: string; ACCURACY: string }
  }
}

// 전역 window에 kakao를 등록 — 각 컴포넌트의 declare global을 여기로 모았다
declare global {
  interface Window {
    kakao: { maps: KakaoMapsSdk }
  }
}
