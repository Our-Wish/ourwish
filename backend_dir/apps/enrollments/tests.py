from datetime import date

from django.test import SimpleTestCase

from apps.enrollments.utils import add_months


class AddMonthsTest(SimpleTestCase):
    """만기일 계산 유틸 add_months 단위 테스트 (DB 불필요 → SimpleTestCase)."""

    def test_normal(self):
        # 평범한 경우: 2026-01-15 + 3개월 = 2026-04-15
        self.assertEqual(add_months(date(2026, 1, 15), 3), date(2026, 4, 15))

    def test_clamp_to_last_day(self):
        # 그달에 없는 날은 말일로: 1/31 + 1개월 → 2/28 (평년)
        self.assertEqual(add_months(date(2026, 1, 31), 1), date(2026, 2, 28))

    def test_clamp_to_last_day_in_leap_year(self):
        # 윤년이면 2월은 29일까지: 2024-01-31 + 1개월 → 2024-02-29
        self.assertEqual(add_months(date(2024, 1, 31), 1), date(2024, 2, 29))

    def test_year_rollover(self):
        # 연도 넘김: 2026-12-10 + 1개월 → 2027-01-10
        self.assertEqual(add_months(date(2026, 12, 10), 1), date(2027, 1, 10))

    def test_full_year(self):
        # 12개월 = 정확히 1년 뒤
        self.assertEqual(add_months(date(2026, 3, 20), 12), date(2027, 3, 20))
