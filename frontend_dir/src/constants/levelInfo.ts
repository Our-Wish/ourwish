export type FilterKey = 'BASE' | 'LOW' | 'MID' | 'HIGH'

export const levelInfo: Record<
  Exclude<FilterKey, 'BASE'>,
  {
    label: string
    title: string
    description: string
    conditions: string[]
  }
> = {
  LOW: {
    label: '쉬움',
    title: '가볍게 챙길 수 있어요',
    description: '앱 가입, 자동이체처럼 대부분 어렵지 않게 완료할 수 있는 조건이에요.',
    conditions: [
      '앱 가입/로그인',
      '자동이체 등록',
      '신규 고객',
      '마케팅 동의',
      '전자통장 발급',
      '입출금 통장 보유',
      '인터넷/모바일뱅킹 가입',
    ],
  },
  MID: {
    label: '보통',
    title: '조금 신경 쓰면 가능해요',
    description: '급여이체나 카드 사용처럼 생활 패턴에 따라 달성 여부가 달라지는 조건이에요.',
    conditions: [
      '급여이체',
      '카드 실적',
      '공과금 자동이체',
      '주택청약 보유',
      '비대면 가입',
      '가족 계좌 연결',
      '적금/예금 동시 보유',
    ],
  },
  HIGH: {
    label: '어려움',
    title: '조건 확인이 필요해요',
    description:
      '기존 자산, 거래 실적, 특정 상품 이용 여부에 따라 달성이 어려울 수 있는 조건이에요.',
    conditions: [
      '높은 카드 사용 실적',
      '외환 거래 실적',
      '대출 보유',
      '자산관리 계좌 보유',
      '프리미엄/VIP 등급',
      '퇴직연금 가입',
      '주택담보대출 연계',
      '증권 연계 계좌',
    ],
  },
}
