// YouTube 제목·채널명은 &#39;(따옴표) 같은 HTML 엔티티 형태로 내려온다.
// 브라우저의 textarea에 한 번 넣었다 빼면 사람이 읽는 글자로 풀린다.
// (백엔드가 이미 풀어줬다면 엔티티가 없으므로 그대로 통과 — 어느 쪽이든 안전)
export function decodeHtmlEntities(text: string): string {
  if (!text) return ''
  const el = document.createElement('textarea')
  el.innerHTML = text
  return el.value
}
