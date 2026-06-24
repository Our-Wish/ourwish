export function formatWon(만원: number): string {
  if (만원 >= 10000) {
    const 억 = Math.floor(만원 / 10000)
    const 나머지 = 만원 % 10000
    return 나머지 > 0 ? `${억}억 ${나머지.toLocaleString()}만원` : `${억}억원`
  }
  return `${만원.toLocaleString()}만원`
}
