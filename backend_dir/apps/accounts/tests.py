from django.test import TestCase

from apps.common.testing import auth_client, make_member, make_profile


class SignupLoginApiTest(TestCase):
    def test_signup_returns_tokens_and_member(self):
        res = auth_client().post(
            "/api/v1/accounts/signup/",
            {"login_id": "newbie", "password": "abcd1234", "nickname": "뉴비"},
            format="json",
        )
        self.assertEqual(res.status_code, 201)
        self.assertIn("access", res.data)
        self.assertEqual(res.data["member"]["login_id"], "newbie")

    def test_signup_rejects_weak_password(self):
        # 8자 미만 / 숫자 없음 / 영문 없음 → 전부 400
        for bad in ("ab12", "abcdefgh", "12345678"):
            res = auth_client().post(
                "/api/v1/accounts/signup/",
                {"login_id": f"u_{bad}", "password": bad, "nickname": "x"},
                format="json",
            )
            self.assertEqual(res.status_code, 400, bad)
            self.assertIn("password", res.data)

    def test_signup_rejects_duplicate_login_id(self):
        make_member(login_id="dup")
        res = auth_client().post(
            "/api/v1/accounts/signup/",
            {"login_id": "dup", "password": "abcd1234", "nickname": "x"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("login_id", res.data)

    def test_login_ok_and_wrong_password(self):
        make_member(login_id="me", password="abcd1234")
        ok = auth_client().post(
            "/api/v1/accounts/login/", {"login_id": "me", "password": "abcd1234"}, format="json"
        )
        bad = auth_client().post(
            "/api/v1/accounts/login/", {"login_id": "me", "password": "wrong000"}, format="json"
        )
        self.assertEqual(ok.status_code, 200)
        self.assertIn("refresh", ok.data)
        self.assertEqual(bad.status_code, 400)


class SearchProfileApiTest(TestCase):
    def setUp(self):
        self.member = make_member()
        self.client = auth_client(self.member)

    def test_deposit_only_profile_without_savings_fields(self):
        # 예금 플로우만 쓰는 회원 — 적금 기간·금액 없이 저장돼야 한다(예전엔 더미 monthly_amount가 필요했음)
        res = self.client.put(
            "/api/v1/search-profile/",
            {"deposit_term": 24, "deposit_amount": 10_000_000, "birth_date": "1999-01-01",
             "first_transaction": True},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["deposit_term"], 24)
        self.assertIsNone(res.data["save_term"])
        self.assertIsNone(res.data["monthly_amount"])

    def test_savings_put_keeps_deposit_fields(self):
        # 적금 저장이 예금 쪽 값을 덮어쓰지 않는다(상품군별 기간 분리)
        make_profile(self.member)
        res = self.client.put(
            "/api/v1/search-profile/",
            {"save_term": 6, "monthly_amount": 100_000, "birth_date": "1999-01-01"},
            format="json",
        )
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data["save_term"], 6)
        self.assertEqual(res.data["deposit_term"], 24)
        self.assertEqual(res.data["deposit_amount"], 10_000_000)

    def test_term_and_amount_must_come_together(self):
        res = self.client.put(
            "/api/v1/search-profile/",
            {"save_term": 12, "birth_date": "1999-01-01"},
            format="json",
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn("save_term", res.data)

    def test_get_without_profile_is_404(self):
        self.assertEqual(self.client.get("/api/v1/search-profile/").status_code, 404)
