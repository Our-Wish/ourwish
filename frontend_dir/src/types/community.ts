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
