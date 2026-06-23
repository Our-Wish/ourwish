export function trimProductName(name: string): string {
  const keywords = ['예금', '적금']
  for (const kw of keywords) {
    const idx = name.indexOf(kw)
    if (idx !== -1) return name.slice(0, idx + kw.length)
  }
  return name
}
