<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 px-4 transition-colors duration-300 md:px-6',
      isHome && !mobileMenuOpen ? 'bg-transparent' : 'bg-[#F7F9FB]',
    ]"
  >
    <!-- 모바일 상단바: 로고 + 햄버거 버튼 (md 미만에서만) -->
    <div class="flex h-14 items-center justify-between md:hidden">
      <RouterLink to="/" class="text-lg font-bold tracking-tight text-slate-900"
        >OURWISH</RouterLink
      >
      <button
        class="flex h-10 w-10 items-center justify-center rounded-xl text-slate-700 transition hover:bg-slate-100"
        :aria-label="mobileMenuOpen ? '메뉴 닫기' : '메뉴 열기'"
        @click="mobileMenuOpen = !mobileMenuOpen"
      >
        <!-- 햄버거(닫힘) / X(열림) 아이콘 -->
        <svg
          v-if="!mobileMenuOpen"
          class="h-6 w-6"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16" />
        </svg>
        <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
          <path stroke-linecap="round" d="M6 6l12 12M18 6L6 18" />
        </svg>
      </button>
    </div>

    <!-- 모바일 펼침 메뉴 -->
    <div
      v-if="mobileMenuOpen"
      class="absolute left-0 right-0 top-14 border-t border-slate-100 bg-[#F7F9FB] pb-4 shadow-lg md:hidden"
    >
      <RouterLink
        to="/depositgoalsetup"
        class="block px-6 py-3.5 text-base font-medium text-slate-700 transition hover:bg-slate-100"
      >
        예금 추천받기
      </RouterLink>
      <RouterLink
        to="/goalsetup"
        class="block px-6 py-3.5 text-base font-medium text-slate-700 transition hover:bg-slate-100"
      >
        적금 추천받기
      </RouterLink>
      <RouterLink
        to="/financelounge"
        class="block px-6 py-3.5 text-base font-medium text-slate-700 transition hover:bg-slate-100"
      >
        금융라운지
      </RouterLink>
      <RouterLink
        to="/mypage"
        class="block px-6 py-3.5 text-base font-medium text-slate-700 transition hover:bg-slate-100"
      >
        마이페이지
      </RouterLink>

      <div class="mx-6 my-2 border-t border-slate-200" />

      <button
        v-if="!isAuthenticated"
        class="block w-full px-6 py-3.5 text-left text-base font-semibold text-blue-700 transition hover:bg-slate-100"
        @click="openLoginFromMobile"
      >
        로그인
      </button>
      <template v-else>
        <p class="px-6 pt-2 pb-1 text-sm font-semibold text-slate-500">
          {{ authStore.user?.nickname }} 님
        </p>
        <button
          class="block w-full px-6 py-3 text-left text-base text-slate-700 transition hover:bg-slate-100"
          @click="openEditProfile"
        >
          회원정보 수정
        </button>
        <button
          class="block w-full px-6 py-3 text-left text-base text-red-500 transition hover:bg-red-50"
          @click="logout"
        >
          로그아웃
        </button>
      </template>
    </div>

    <!-- 데스크탑 바 (md 이상에서만) -->
    <div class="mx-auto hidden h-16 max-w-6xl items-center justify-between md:flex">
      <RouterLink to="/" class="text-xl font-bold tracking-tight text-slate-900"
        >OURWISH</RouterLink
      >

      <div class="flex items-center gap-4">
        <RouterLink
          to="/depositgoalsetup"
          class="rounded-2xl px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100 hover:font-semibold"
        >
          예금 추천받기
        </RouterLink>

        <RouterLink
          to="/goalsetup"
          class="rounded-2xl px-4 py-2 text-base font-normal text-slate-700 transition hover:bg-slate-100 hover:font-semibold"
        >
          적금 추천받기
        </RouterLink>
        <div
          class="relative"
          @mouseenter="loungeDropdownOpen = true"
          @mouseleave="loungeDropdownOpen = false"
        >
          <RouterLink
            to="/financelounge"
            class="block rounded-2xl px-4 py-2 text-base font-normal text-slate-700 transition hover:font-semibold hover:text-blue-800"
          >
            금융라운지
          </RouterLink>
          <div
            v-if="loungeDropdownOpen"
            class="absolute left-0 top-full w-36 overflow-hidden rounded-xl bg-white shadow-lg ring-1 ring-slate-200"
          >
            <RouterLink
              to="/financelounge?tab=video"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              금융TV
            </RouterLink>
            <RouterLink
              to="/financelounge?tab=goldsilver"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              금/은 시세
            </RouterLink>
            <RouterLink
              to="/financelounge?tab=community"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              커뮤니티
            </RouterLink>
          </div>
        </div>
        <div
          class="relative"
          @mouseenter="mypageDropdownOpen = true"
          @mouseleave="mypageDropdownOpen = false"
        >
          <RouterLink
            to="/mypage"
            class="block rounded-2xl px-4 py-2 text-base font-semibold text-slate-700 transition hover:font-semibold hover:text-blue-800"
          >
            마이페이지
          </RouterLink>
          <div
            v-if="mypageDropdownOpen"
            class="absolute left-0 top-full w-44 overflow-hidden rounded-xl bg-white shadow-lg ring-1 ring-slate-200"
          >
            <RouterLink
              to="/mypage?tab=products"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              나의 금융상품
            </RouterLink>
            <RouterLink
              to="/mypage?tab=marketRate"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              가입 상품 금리 비교
            </RouterLink>
            <RouterLink
              to="/mypage?tab=wishlist"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              찜한 상품
            </RouterLink>
            <RouterLink
              to="/mypage?tab=videos"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              찜한 영상
            </RouterLink>
            <RouterLink
              to="/mypage?tab=posts"
              class="block px-4 py-3 text-base text-slate-700 transition hover:bg-slate-50"
            >
              작성한 글
            </RouterLink>
          </div>
        </div>

        <button
          v-if="!isAuthenticated"
          class="rounded-full px-4 py-2 text-base font-semibold text-slate-700 transition hover:bg-slate-100 hover:font-semibold"
          @click="authStore.openLoginModal()"
        >
          로그인
        </button>

        <div
          v-else
          class="relative"
          ref="dropdownRef"
          @mouseenter="dropdownOpen = true"
          @mouseleave="dropdownOpen = false"
        >
          <button
            class="flex items-center gap-1.5 px-4 py-2 text-base font-semibold text-slate-700 transition cursor-pointer hover:text-blue-800 hover:font-semibold"
          >
            {{ authStore.user?.nickname }} 님
          </button>

          <div
            v-if="dropdownOpen"
            class="absolute rounded-xl right-0 top-full w-40 overflow-hidden bg-white shadow-lg ring-1 ring-slate-200"
          >
            <button
              @click="openEditProfile"
              class="w-full px-4 py-3 text-left text-base text-slate-700 transition hover:bg-slate-50"
            >
              회원정보 수정
            </button>
            <button
              @click="logout"
              class="w-full px-4 py-3 text-left text-base text-red-500 transition hover:bg-red-50"
            >
              로그아웃
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <EditProfileModal v-if="showEditProfile" @close="showEditProfile = false" />
</template>

<script setup lang="ts">
import { computed, ref, watch, onMounted, onBeforeUnmount } from 'vue'
import { storeToRefs } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import EditProfileModal from '@/components/EditProfileModal.vue'

const authStore = useAuthStore()
const { isAuthenticated } = storeToRefs(authStore)
const route = useRoute()
const router = useRouter()
const isHome = computed(() => route.path === '/')

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement | null>(null)
const showEditProfile = ref(false)

const loungeDropdownOpen = ref(false)
const mypageDropdownOpen = ref(false)

// 모바일 햄버거 메뉴 열림 상태. 페이지를 이동하면 자동으로 닫는다.
const mobileMenuOpen = ref(false)
watch(() => route.fullPath, () => {
  mobileMenuOpen.value = false
})

const openLoginFromMobile = () => {
  mobileMenuOpen.value = false
  authStore.openLoginModal()
}

const openEditProfile = () => {
  dropdownOpen.value = false
  mobileMenuOpen.value = false
  showEditProfile.value = true
}

const logout = () => {
  dropdownOpen.value = false
  mobileMenuOpen.value = false
  authStore.logout()
  router.push('/')
}

const handleClickOutside = (e: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    dropdownOpen.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', handleClickOutside))
onBeforeUnmount(() => document.removeEventListener('mousedown', handleClickOutside))
</script>
