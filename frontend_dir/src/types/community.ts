export type Post = {
  id: number
  title: string
  content: string
  authorNickname: string
  createdAt: string
  commentCount: number
}

export type PostDetail = Post & {
  authorId: number
}

export type Comment = {
  id: number
  authorId: number
  authorNickname: string
  content: string
  createdAt: string
}
