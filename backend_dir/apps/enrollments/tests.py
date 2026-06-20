from datetime import date

from django.test import SimpleTestCase

from apps.enrollments.utils import calculate_achievement_gauge, months_between


class MonthsBetweenTest(SimpleTestCase):
    """경과 개월 계산 단위 테스트 (DB 불필요 → SimpleTestCase)."""

    def test_exact_year(self):
        self.assertEqual(months_between(date(2025, 6, 20), date(2026, 6, 20)), 12)

    def test_one_day_short(self):
        # 하루 모자라면 한 달 덜 친다: 11개월
        self.assertEqual(months_between(date(2025, 6, 20), date(2026, 6, 19)), 11)

    def test_end_before_start(self):
        self.assertEqual(months_between(date(2026, 1, 1), date(2025, 1, 1)), 0)


class AchievementGaugeTest(SimpleTestCase):
    """달성 게이지(금액 기반=개월 비율) 단위 테스트."""

    def test_half_way(self):
        # 1년 적금, 6개월 경과 → 50%
        gauge = calculate_achievement_gauge(
            date(2025, 1, 1), date(2026, 1, 1), today=date(2025, 7, 1)
        )
        self.assertEqual(gauge, 50.0)

    def test_capped_at_100(self):
        # 만기를 지나도 100%를 넘지 않는다
        gauge = calculate_achievement_gauge(
            date(2025, 1, 1), date(2026, 1, 1), today=date(2027, 1, 1)
        )
        self.assertEqual(gauge, 100.0)

    def test_not_started(self):
        # 시작 전이면 0%
        gauge = calculate_achievement_gauge(
            date(2025, 1, 1), date(2026, 1, 1), today=date(2024, 12, 1)
        )
        self.assertEqual(gauge, 0.0)
