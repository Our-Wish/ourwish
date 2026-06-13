<template>
  <div class="min-h-screen bg-slate-50 pb-10">
    <header class="flex items-center px-5 py-4">
      <button @click="router.go(-1)" class="flex items-center gap-1 text-sm text-slate-600">
        <span>‹</span>
        <span>뒤로</span>
      </button>
    </header>

    <div class="px-5 pt-2">
      <!-- 인사말 -->
      <h1 class="mt-1 text-3xl font-extrabold text-slate-900">
        <template v-if="goalStore.targetAmount">
          지금까지 벌써 <span class="text-blue-500">{{ progressPercent }}%</span> 모았어요!
        </template>
        <template v-else>목표를 설정해봐요!</template>
      </h1>

      <!-- 목표 카드 (다크) -->
      <div class="mt-5 rounded-3xl bg-[#111827] p-6 text-white">
        <!-- 목표 없음 상태 -->
        <template v-if="!goalStore.targetAmount && !isEditing">
          <p class="text-sm font-semibold text-slate-300">아직 목표 금액이 없어요</p>
          <p class="mt-1.5 text-sm text-slate-400">얼마를 목표로 모아볼까요?</p>
          <button
            @click="startEditing"
            class="mt-5 w-full rounded-2xl bg-blue-600 py-3.5 text-base font-semibold transition hover:bg-blue-500"
          >
            목표 설정하기
          </button>
        </template>

        <!-- 인라인 입력 상태 -->
        <template v-else-if="isEditing">
          <p class="text-sm text-slate-400">최종 목표 금액을 입력해주세요</p>
          <div class="mt-4 flex items-center gap-2">
            <input
              ref="inputRef"
              v-model.number="inputAmount"
              type="number"
              min="1"
              placeholder="0"
              class="w-full rounded-xl bg-white/10 px-4 py-3 text-3xl font-bold text-white placeholder-white/30 outline-none focus:ring-2 focus:ring-blue-500"
            />
            <span class="shrink-0 text-xl font-semibold text-slate-300">만원</span>
          </div>
          <div class="mt-3 flex gap-2">
            <button
              v-for="preset in presets"
              :key="preset"
              @click="inputAmount = preset"
              class="rounded-full px-3 py-1 text-sm font-medium transition"
              :class="
                inputAmount === preset
                  ? 'bg-blue-600 text-white'
                  : 'bg-white/10 text-slate-300 hover:bg-white/20'
              "
            >
              {{ preset.toLocaleString() }}만
            </button>
          </div>
          <div class="mt-5 flex gap-2">
            <button
              @click="cancelEditing"
              class="flex-1 rounded-xl border border-white/20 py-3 text-sm font-medium text-slate-300 transition hover:bg-white/10"
            >
              취소
            </button>
            <button
              @click="saveGoal"
              :disabled="!inputAmount || inputAmount <= 0"
              class="flex-[2] rounded-xl bg-blue-600 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:opacity-40"
            >
              저장하기
            </button>
          </div>
        </template>

        <!-- 목표 설정 완료 상태 -->
        <template v-else>
          <div class="flex items-start justify-between">
            <div>
              <p class="text-xs text-slate-400">최종 목표</p>
              <p class="mt-0.5 text-xl font-bold">
                {{ goalStore.targetAmount.toLocaleString() }}만원
              </p>
            </div>
            <button
              @click="startEditing"
              class="rounded-full bg-white/10 px-4 py-1.5 text-xs font-medium transition hover:bg-white/20"
            >
              수정
            </button>
          </div>

          <p class="mt-5 text-xs text-slate-400">지금까지 모은 금액</p>
          <p class="mt-1 text-4xl font-extrabold">{{ currentSavings.toLocaleString() }}원</p>

          <div class="mt-4 h-2 overflow-hidden rounded-full bg-white/20">
            <div
              class="h-full rounded-full transition-all duration-500"
              :style="{
                width: `${progressPercent}%`,
                background: 'linear-gradient(to right, #FBBF24, #F87171)',
              }"
            />
          </div>

          <p class="mt-3 text-xs text-slate-300">현재 적금으로 목표 달성 가능해요 ✨</p>
        </template>
      </div>

      <!-- 통계 행 -->
      <div class="mt-4 grid grid-cols-3 gap-3">
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-xs text-slate-400">가입 상품</p>
          <p class="mt-1 text-lg font-bold text-slate-900">{{ subscribedCount }}개</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-xs text-slate-400">이번 달 납입</p>
          <p class="mt-1 text-lg font-bold text-slate-900">{{ monthlyPayment }}만원</p>
        </div>
        <div class="rounded-2xl border border-slate-200 bg-white px-3 py-4 text-center">
          <p class="text-xs text-slate-400">빠른 만기</p>
          <p class="mt-1 text-lg font-bold text-slate-900">D-{{ nearestMaturity }}</p>
        </div>
      </div>

      <!-- 진행 중인 적금 -->
      <div class="mt-8">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-900">진행 중인 적금</h2>
          <button
            @click="router.push({ name: 'recommendation' })"
            class="rounded-full bg-slate-100 px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-200 transition"
          >
            + 추가
          </button>
        </div>

        <!-- 적금 카드 -->
        <SavingsCard
          class="mt-3"
          bankInitial="카"
          bankColor="#F9E000"
          bankName="카카오뱅크"
          productName="카뱅 26주적금"
          :dDay="124"
          :currentAmount="28"
          :maturityAmount="30"
          :progress="93"
          nextPaymentDate="12월 25일"
          :monthlyAmount="5"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useGoalStore } from '@/stores/goal'
import SavingsCard from '@/components/MyPage/SavingsCard.vue'

const router = useRouter()
const authStore = useAuthStore()
const goalStore = useGoalStore()

const isEditing = ref(false)
const inputAmount = ref<number | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const presets = [500, 1000, 2000, 5000]

// 나중에 백엔드 연동 예정
const currentSavings = 1000000
const subscribedCount = 3
const monthlyPayment = 105
const nearestMaturity = 124

const progressPercent = computed(() => {
  if (!goalStore.targetAmount) return 0
  return Math.min(100, Math.round((currentSavings / (goalStore.targetAmount * 10000)) * 100))
})

function startEditing() {
  inputAmount.value = goalStore.targetAmount || null
  isEditing.value = true
  nextTick(() => inputRef.value?.focus())
}

function cancelEditing() {
  isEditing.value = false
  inputAmount.value = null
}

function saveGoal() {
  if (!inputAmount.value || inputAmount.value <= 0) return
  goalStore.setTargetAmount(inputAmount.value)
  isEditing.value = false
  inputAmount.value = null
}
</script>
