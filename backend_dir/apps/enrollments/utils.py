"""가입(Enrollment) 도메인에서 쓰는 날짜 계산 유틸.

만기일(maturity_date)은 #10 목록 조회와 #13 마이페이지가 모두 쓰므로
한 곳에 모아 두고 재사용한다.
"""
import calendar
from datetime import date


def add_months(base_date, months):
    """base_date에 months개월을 더한 날짜를 돌려준다.

    파이썬 기본 date에는 '몇 개월 더하기'가 없어서 직접 계산한다.
    1월 31일 + 1개월처럼 그달에 없는 날이 되면 그달의 말일로 맞춘다.
    (예: 2025-01-31 + 1개월 → 2025-02-28)
    """
    # 0부터 세는 '달 인덱스'로 바꿔 계산하면 연도 넘김이 쉽다.
    # 예: 2025-12(=index 11) + 1 → index 12 → 2026-01
    month_index = base_date.month - 1 + months
    year = base_date.year + month_index // 12   # 12로 나눈 몫 = 넘어간 연도 수
    month = month_index % 12 + 1                 # 나머지 = 그 해의 달(1~12)

    # 그 달의 마지막 날(28~31)을 구해 day가 넘치지 않게 자른다.
    last_day = calendar.monthrange(year, month)[1]
    day = min(base_date.day, last_day)
    return date(year, month, day)
