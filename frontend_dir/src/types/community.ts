// 목록 한 줄 (GET /community/posts/)
export type Post = {
  id: number
  title: string
  authorId: number
  authorNickname: string
  createdAt: string
  commentCount: number
}

// 댓글 한 줄
export type Comment = {
  id: number
  authorId: number
  authorNickname: string
  content: string
  createdAt: string
}

// 글 상세 (GET /community/posts/:id/) — 본문 + 댓글 전체
export type PostDetail = {
  id: number
  title: string
  content: string
  authorId: number
  authorNickname: string
  comments: Comment[]
  createdAt: string
}

// ── 백엔드 원본 응답(snake_case) ──
// API가 내려주는 모양 그대로. 화면용 타입(camelCase)으로 바꾸기 전 단계에서 쓴다.

// 목록 한 줄 원본 (GET /community/posts/)
export type PostApi = {
  id: number
  title: string
  author_id: number
  author_nickname: string
  comment_count: number
  created_at: string
}

// 댓글 한 줄 원본
export type CommentApi = {
  id: number
  author_id: number
  author_nickname: string
  content: string
  created_at: string
}
