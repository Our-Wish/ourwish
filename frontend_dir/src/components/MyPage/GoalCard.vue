<template>
  <div class="rounded-3xl bg-[#111827] p-6 text-white">
    <!-- 목표 없음 상태 -->
    <template v-if="!goalStore.targetAmount && !isEditing">
      <p class="text-lg font-semibold text-slate-300">목표 금액을 설정해보세요</p>
      <p class="mt-1.5 text-base text-slate-400">진행률과 만기 수령액을 한눈에 확인할 수 있어요.</p>
      <button
        @click="startEditing"
        class="mt-5 w-full rounded-2xl bg-blue-600 py-3.5 text-base font-semibold transition hover:bg-blue-500"
      >
        목표 설정하기
      </button>
    </template>

    <!-- 인라인 입력 상태 -->
    <template v-else-if="isEditing">
      <p class="text-base text-slate-400">최종 목표 금액을 입력해주세요</p>
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
          class="rounded-full px-3 py-1 text-base font-medium transition"
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
          class="flex-1 rounded-xl border border-white/20 py-3 text-base font-medium text-slate-300 transition hover:bg-white/10"
        >
          취소
        </button>
        <button
          @click="saveGoal"
          :disabled="!inputAmount || inputAmount <= 0"
          class="flex-[2] rounded-xl bg-blue-600 py-3 text-base font-semibold transition hover:bg-blue-500 disabled:opacity-40"
        >
          저장하기
        </button>
      </div>
    </template>

    <!-- 목표 설정 완료 상태 -->
    <template v-else>
      <div class="flex items-start justify-between">
        <div>
          <p class="text-lg text-slate-400">목표 금액</p>
          <p class="mt-0.5 text-2xl font-bold">{{ goalStore.targetAmount.toLocaleString() }}만원</p>
        </div>
        <button
          @click="startEditing"
          class="rounded-full bg-white/10 px-4 py-1.5 text-sm font-medium transition hover:bg-white/20"
        >
          수정
        </button>
      </div>

      <p class="mt-5 text-base text-slate-400">현재 모은 금액</p>
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

      <p class="mt-5 text-sm text-slate-300">예정대로 납입하면 목표에 도달할 수 있어요✨</p>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { useGoalStore } from '@/stores/goal'

const props = defineProps<{ currentSavings: number }>()

const goalStore = useGoalStore()

const isEditing = ref(false)
const inputAmount = ref<number | null>(null)
const inputRef = ref<HTMLInputElement | null>(null)

const presets = [500, 1000, 2000, 5000]

const progressPercent = computed(() => {
  if (!goalStore.targetAmount) return 0
  return Math.min(100, Math.round((props.currentSavings / (goalStore.targetAmount * 10000)) * 100))
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
