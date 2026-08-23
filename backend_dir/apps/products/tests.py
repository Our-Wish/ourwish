from django.test import SimpleTestCase

from apps.products.models import ProductOption
from apps.products.services import calculate_after_tax_payout
from apps.products.views import _has_conditions


class AfterTaxPayoutTest(SimpleTestCase):
    """만기 세후 수령액 계산 단위 테스트 (DB 불필요 → SimpleTestCase)."""

    MONTHLY = 100_000  # 월 납입액
    TERM = 12          # 납입 개월 수

    def test_simple_interest(self):
        # 단리 3.0%: 원금 120만 + 세후이자 → 1,216,497원
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 3.0, ProductOption.IntrRateType.SIMPLE
        )
        self.assertEqual(result, 1_216_497)

    def test_compound_interest(self):
        # 복리(월복리) 3.0% → 1,214,075원
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 3.0, ProductOption.IntrRateType.COMPOUND
        )
        self.assertEqual(result, 1_214_075)

    def test_zero_rate_returns_principal(self):
        # 이율 0% → 이자 없이 원금(120만)만 (0 나눗셈 방어 동작 확인)
        result = calculate_after_tax_payout(
            self.MONTHLY, self.TERM, 0, ProductOption.IntrRateType.SIMPLE
        )
        self.assertEqual(result, 1_200_000)


class HasConditionsTest(SimpleTestCase):
    """우대조건 유무 판정 — 무조건 상품을 추천 OR필터에 통과시킬 때 사용."""

    def test_no_condition_markers(self):
        # 비어있거나 '없음'류(앞뒤 공백 포함)·None → 우대조건 없음
        for raw in ["", "   ", "없음", " 해당없음 ", None]:
            self.assertFalse(_has_conditions(raw))

    def test_real_conditions(self):
        self.assertTrue(_has_conditions("급여이체: 연 0.3%p"))


from django.test import TestCase

from apps.common.testing import auth_client, make_member, make_product, make_profile
from apps.products.models import Product


class RecommendApiTest(TestCase):
    """추천 API — 비로그인(쿼리 조건)·로그인(프로필) 두 경로."""

    def setUp(self):
        # 12개월 옵션이 있는 적금 2개(급여이체 태그 유무), 예금 1개
        self.salary = make_product("급여적금", tag_salary_transfer=True,
                                   special_condition_raw="급여이체 시 우대")
        self.plain = make_product("무조건적금", special_condition_raw="")
        self.deposit = make_product("테스트예금", product_type=Product.ProductType.DEPOSIT, terms=(24,))

    def test_anonymous_with_criteria(self):
        res = auth_client().get(
            "/api/v1/products/recommend/",
            {"save_term": 12, "amount": 300_000, "salary_transfer": "true", "page_size": 50},
        )
        self.assertEqual(res.status_code, 200)
        names = [r["product_name"] for r in res.data["results"]]
        self.assertIn("급여적금", names)
        self.assertIn("무조건적금", names)  # 우대조건 없는 상품은 OR 매칭에서 통과
        self.assertNotIn("테스트예금", names)

    def test_anonymous_without_criteria_is_400(self):
        self.assertEqual(auth_client().get("/api/v1/products/recommend/").status_code, 400)

    def test_term_and_amount_pair_required(self):
        res = auth_client().get("/api/v1/products/recommend/", {"save_term": 12})
        self.assertEqual(res.status_code, 400)

    def test_logged_in_uses_profile_per_product_type(self):
        member = make_member()
        make_profile(member)  # 적금 12개월 / 예금 24개월
        client = auth_client(member)
        savings = client.get("/api/v1/products/recommend/", {"product_type": "SAVINGS"})
        deposit = client.get("/api/v1/products/recommend/", {"product_type": "DEPOSIT"})
        self.assertEqual(savings.status_code, 200)
        self.assertEqual([r["save_term"] for r in savings.data["results"]], [12, 12])
        self.assertEqual([r["product_name"] for r in deposit.data["results"]], ["테스트예금"])
        self.assertEqual(deposit.data["results"][0]["save_term"], 24)

    def test_sort_all_requires_every_tag(self):
        res = auth_client().get(
            "/api/v1/products/recommend/",
            {"save_term": 12, "amount": 300_000, "salary_transfer": "true", "sort": "all"},
        )
        self.assertEqual([r["product_name"] for r in res.data["results"]], ["급여적금"])

    def test_detail_is_public_and_not_favorited(self):
        res = auth_client().get(f"/api/v1/products/{self.salary.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertFalse(res.data["is_favorited"])
        self.assertEqual(res.data["max_rate"], 4.0)
