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


from django.test import TestCase

from apps.common.testing import auth_client, make_member, make_product
from apps.enrollments.models import Enrollment


class EnrollmentApiTest(TestCase):
    def setUp(self):
        self.member = make_member()
        self.client = auth_client(self.member)
        self.product = make_product()

    def test_register_then_fill_then_delete(self):
        reg = self.client.post("/api/v1/enrollments/", {"product_id": self.product.id}, format="json")
        self.assertEqual(reg.status_code, 201)
        self.assertFalse(reg.data["is_filled"])
        self.assertEqual(reg.data["max_rate"], 4.0)  # 목록/등록 응답에 대표 금리 포함
        eid = reg.data["enrollment_id"]

        dup = self.client.post("/api/v1/enrollments/", {"product_id": self.product.id}, format="json")
        self.assertEqual(dup.status_code, 409)

        fill = self.client.patch(
            f"/api/v1/enrollments/{eid}/",
            {"monthly_amount": 500_000, "rate": "3.5", "start_date": "2026-01-01",
             "maturity_date": "2027-01-01"},
            format="json",
        )
        self.assertEqual(fill.status_code, 200)
        self.assertTrue(fill.data["is_filled"])
        self.assertIsNone(fill.data["deposit_amount"])  # 적금이면 예치금액은 비워진다

        self.assertEqual(self.client.delete(f"/api/v1/enrollments/{eid}/").status_code, 204)
        self.assertFalse(Enrollment.objects.filter(id=eid).exists())

    def test_cannot_touch_others_enrollment(self):
        other = make_member(login_id="other")
        e = Enrollment.objects.create(member=other, product=self.product)
        self.assertEqual(self.client.delete(f"/api/v1/enrollments/{e.id}/").status_code, 403)

    def test_maturity_must_be_after_start(self):
        e = Enrollment.objects.create(member=self.member, product=self.product)
        res = self.client.patch(
            f"/api/v1/enrollments/{e.id}/",
            {"monthly_amount": 1, "rate": "1", "start_date": "2026-01-01", "maturity_date": "2026-01-01"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
