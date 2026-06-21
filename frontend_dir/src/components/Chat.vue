<template>
  <div class="flex flex-col">
    <div ref="listEl" class="relative h-80 overflow-y-auto p-4">
      <img
        src="@/assets/img/wishes/hiWish.png"
        class="pointer-events-none absolute bottom-2 right-2 h-40 w-40 select-none object-contain opacity-10"
      />

      <template v-if="messages.length === 0">
        <div class="flex justify-start">
          <div
            class="max-w-[85%] rounded-2xl rounded-bl-sm bg-blue-50 px-4 py-3 text-base leading-relaxed text-slate-700"
          >
            안녕하세요! 👋<br />
            이 상품의 금리, 우대조건,<br />
            가입방법을 쉽게 설명해드릴게요.
          </div>
        </div>
        <div class="mt-3 flex flex-col gap-2">
          <button
            v-for="q in quickQuestions"
            :key="q"
            @click="setQuestion(q)"
            class="rounded-full border border-blue-200 px-4 py-2 text-left text-base text-blue-500 transition hover:bg-blue-50"
          >
            {{ q }}
          </button>
        </div>
      </template>

      <div
        v-for="(m, i) in messages"
        :key="i"
        class="flex"
        :class="m.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          class="mt-2 max-w-[80%] whitespace-pre-line rounded-2xl px-4 py-2.5 text-base"
          :class="
            m.role === 'user'
              ? 'rounded-br-sm bg-blue-400 text-white'
              : 'rounded-bl-sm bg-blue-50 text-slate-800'
          "
        >
          <span>{{ m.content }}</span>
          <span v-if="loading && i === messages.length - 1 && !m.content" class="text-slate-400"
            >···</span
          >
        </div>
      </div>
    </div>

    <form
      @submit.prevent="sendMessage"
      class="flex items-center gap-2 border-t border-slate-100 px-4 py-3"
    >
      <input
        v-model="input"
        :disabled="loading"
        placeholder="이 상품에 대해 궁금한 점을 입력해보세요"
        class="flex-1 rounded-full border border-slate-200 px-4 py-2.5 text-base focus:border-blue-300 focus:outline-none"
      />
      <button
        type="submit"
        :disabled="loading || !input.trim()"
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-400 text-white transition hover:bg-blue-300 disabled:opacity-40"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="h-5 w-5"
        >
          <path
            d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z"
          />
        </svg>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'

const props = defineProps<{ productId: number }>()

type ChatMessage = { role: 'user' | 'assistant'; content: string }

const messages = ref<ChatMessage[]>([])
const input = ref('')
const loading = ref(false)
const listEl = ref<HTMLElement | null>(null)

const quickQuestions = [
  '우대금리를 받으려면 무엇을 해야 하나요?',
  '이 상품의 장점과 단점을 알려주세요.',
  '만기 후 이자율을 쉽게 설명해주세요',
]

function setQuestion(q: string) {
  input.value = q
  sendMessage()
}

async function scrollToBottom() {
  await nextTick()
  listEl.value?.scrollTo(0, listEl.value.scrollHeight)
}

const TICK_MS = 20
const CHARS_PER_TICK = 1

async function sendMessage() {
  const text = input.value.trim()
  if (!text || loading.value) return

  messages.value.push({ role: 'user', content: text })
  input.value = ''
  loading.value = true

  messages.value.push({ role: 'assistant', content: '' })
  const bot = messages.value[messages.value.length - 1]!
  await scrollToBottom()

  let pending = ''
  let streamDone = false

  const timer = window.setInterval(() => {
    if (pending.length > 0) {
      bot.content += pending.slice(0, CHARS_PER_TICK)
      pending = pending.slice(CHARS_PER_TICK)
      scrollToBottom()
    } else if (streamDone) {
      window.clearInterval(timer)
      loading.value = false
    }
  }, TICK_MS)

  try {
    const base = import.meta.env.VITE_API_BASE_URL ?? ''
    const token = sessionStorage.getItem('auth_token')
    const res = await fetch(`${base}/api/v1/products/${props.productId}/chat/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify({ messages: messages.value.slice(0, -1) }),
    })
    if (!res.ok || !res.body) throw new Error(`chat failed: ${res.status}`)

    const reader = res.body.getReader()
    const decoder = new TextDecoder()
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      pending += decoder.decode(value, { stream: true })
    }
  } catch {
    pending = ''
    bot.content = '죄송해요, 답변을 가져오지 못했어요. 잠시 후 다시 시도해 주세요.'
  } finally {
    streamDone = true
  }
}
</script>
