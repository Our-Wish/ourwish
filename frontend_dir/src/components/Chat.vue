<template>
  <div class="mt-8">
    <div class="flex items-center gap-2">
      <span class="rounded-lg bg-indigo-500 px-2 py-0.5 text-xs font-bold text-white">AI</span>
      <span class="text-sm font-semibold text-indigo-500">이 상품, 무엇이든 물어보세요</span>
    </div>

    <div class="mt-3 overflow-hidden rounded-2xl border border-slate-200 bg-white">
      <!-- 대화 영역 -->
      <div ref="listEl" class="h-72 space-y-3 overflow-y-auto p-4">
        <p v-if="messages.length === 0" class="py-10 text-center text-sm text-slate-400">
          예: "중도해지하면 어떻게 돼?", "우대금리 받으려면?"
        </p>
        <div
          v-for="(m, i) in messages"
          :key="i"
          class="flex"
          :class="m.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-[80%] whitespace-pre-line rounded-2xl px-4 py-2 text-sm"
            :class="
              m.role === 'user'
                ? 'rounded-br-sm bg-blue-500 text-white'
                : 'rounded-bl-sm bg-slate-100 text-slate-800'
            "
          >
            <span>{{ m.content }}</span>
            <!-- 답변 도착 전 깜빡이는 표시 -->
            <span
              v-if="loading && i === messages.length - 1 && !m.content"
              class="text-slate-400"
              >···</span
            >
          </div>
        </div>
      </div>

      <!-- 입력창 -->
      <form
        @submit.prevent="sendMessage"
        class="flex items-center gap-2 border-t border-slate-100 p-3"
      >
        <input
          v-model="input"
          :disabled="loading"
          placeholder="이 상품에 대해 물어보세요"
          class="flex-1 rounded-xl border border-slate-200 px-3 py-2 text-sm focus:border-blue-400 focus:outline-none"
        />
        <button
          type="submit"
          :disabled="loading || !input.trim()"
          class="rounded-xl bg-blue-500 px-4 py-2 text-sm font-semibold text-white transition hover:bg-blue-400 disabled:opacity-40"
        >
          전송
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

// 부모(상품상세 뷰)가 어떤 상품인지 내려준다.
const props = defineProps<{ productId: number }>()

type ChatMessage = { role: 'user' | 'assistant'; content: string }

const messages = ref<ChatMessage[]>([]) // 대화 보관 = "기억" (모달/뷰 떠날 때 소멸)
const input = ref('')
const loading = ref(false)
const listEl = ref<HTMLElement | null>(null)

async function scrollToBottom() {
  await nextTick() // 화면 갱신 후
  listEl.value?.scrollTo(0, listEl.value.scrollHeight)
}

// v 타이핑 속도: TICK_MS마다 CHARS_PER_TICK 글자씩 화면에 푼다.
//   빠르게 하려면 CHARS_PER_TICK을 늘리거나, TICK_MS를 줄이거나.
const TICK_MS = 20
const CHARS_PER_TICK = 1

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  // 1) 내 질문 추가
  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  // 2) 빈 봇 말풍선 먼저 만들기 (조각이 여기로 흘러들어옴)
  messages.value.push({ role: 'assistant', content: '' })
  const bot = messages.value[messages.value.length - 1] // ★ 반응형 프록시를 잡아야 화면 갱신됨
  await scrollToBottom()

  let pending = '' // 받았지만 아직 화면에 안 푼 글자(버퍼)
  let streamDone = false // 서버 스트림이 끝났는지

  // 받는 속도와 무관하게, 일정 간격으로 버퍼에서 조금씩 꺼내 보여줌 = 부드러운 타자기
  const timer = window.setInterval(() => {
    if (pending.length > 0) {
      bot.content += pending.slice(0, CHARS_PER_TICK)
      pending = pending.slice(CHARS_PER_TICK)
      scrollToBottom()
    } else if (streamDone) {
      // 버퍼 다 비웠고 스트림도 끝남 → 타자기 종료
      window.clearInterval(timer)
      loading.value = false
    }
  }, TICK_MS)

  try {
    const base = import.meta.env.VITE_API_BASE_URL ?? ''
    const token = sessionStorage.getItem('auth_token') // 기존 api 인스턴스와 동일한 키
    // 스트리밍은 axios로 못 받으니 fetch 사용
    const res = await fetch(`${base}/api/v1/products/${props.productId}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      // 방금 만든 빈 봇 말풍선은 빼고(slice) 지금까지 대화를 통째로 전송
      body: JSON.stringify({ messages: messages.value.slice(0, -1) }),
    })
    if (!res.ok || !res.body) throw new Error(`chat failed: ${res.status}`)

    // 3) 받은 건 '버퍼에만' 쌓고, 화면 노출은 위 타이머가 일정 속도로 처리
    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      // {stream:true} = 한글(멀티바이트)이 조각 경계에서 쪼개져도 안전하게 이어줌
      pending += decoder.decode(value, { stream: true })
    }
  } catch {
    pending = ''
    bot.content = '죄송해요, 답변을 가져오지 못했어요. 잠시 후 다시 시도해 주세요.'
  } finally {
    // 타이머가 남은 버퍼를 다 비우면 스스로 종료하며 loading을 해제한다
    streamDone = true
  }
}
</script>
