"""가입(Enrollment) 도메인 날짜·게이지 유틸."""
from datetime import date


def months_between(start, end):
    """start~end 사이 '완료된 개월 수'. end가 start보다 이르거나 같으면 0.

    예: 2025-06-20 ~ 2026-06-20 → 12개월. 2025-06-20 ~ 2026-06-19 → 11개월(하루 모자람).
    """
    if end <= start:
        return 0
    months = (end.year - start.year) * 12 + (end.month - start.month)
    if end.day < start.day:  # 일(day)이 아직 안 찼으면 한 달 덜 친다
        months -= 1
    return max(months, 0)


def calculate_achievement_gauge(start_date, maturity_date, today=None):
    """달성 게이지(%) — 금액 기반.

    월납입액이 일정하다고 보면
      (월납입 × 경과개월) / (월납입 × 총개월) = 경과개월 / 총개월
    이라 개월 비율로 계산한다. 만기를 지났으면 100%로 막는다.
    """
    today = today or date.today()
    total = months_between(start_date, maturity_date)
    if total <= 0:
        return 0.0
    elapsed = min(months_between(start_date, today), total)
    return round(elapsed / total * 100, 1)
