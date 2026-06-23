<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 px-6 transition-colors duration-300',
      isHome ? 'bg-transparent' : 'bg-[#F7F9FB]',
    ]"
  >
    <div class="mx-auto flex h-16 max-w-6xl items-center justify-between">
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
        <!-- 금융라운지 드롭다운 -->
        <div
          class="relative"
          @mouseenter="loungeDropdownOpen = true"
          @mouseleave="loungeDropdownOpen = false"
        >
          <RouterLink
            to="/financelounge"
            class="block rounded-2xl px-4 py-2 text-base font-semibold text-slate-700 transition hover:font-semibold hover:text-blue-800"
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
        <!-- 마이페이지 드롭다운 -->
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
import { computed, ref, onMounted, onBeforeUnmount } from 'vue'
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

const openEditProfile = () => {
  dropdownOpen.value = false
  showEditProfile.value = true
}

const logout = () => {
  dropdownOpen.value = false
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
