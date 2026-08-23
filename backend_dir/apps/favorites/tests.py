from django.test import TestCase

from apps.common.testing import auth_client, make_member, make_product
from apps.favorites.models import Favorite


class FavoriteApiTest(TestCase):
    def setUp(self):
        self.member = make_member()
        self.client = auth_client(self.member)
        self.product = make_product()

    def test_add_list_delete(self):
        add = self.client.post("/api/v1/favorites/", {"product_id": self.product.id}, format="json")
        self.assertEqual(add.status_code, 201)
        # 중복 추가는 그대로 유지(201이지만 1건)
        self.client.post("/api/v1/favorites/", {"product_id": self.product.id}, format="json")
        self.assertEqual(Favorite.objects.filter(member=self.member).count(), 1)

        listed = self.client.get("/api/v1/favorites/")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.data[0]["product_name"], "테스트적금")
        self.assertEqual(listed.data[0]["max_rate"], 4.0)

        delete = self.client.delete(f"/api/v1/favorites/{self.product.id}/")
        self.assertEqual(delete.status_code, 204)
        self.assertEqual(Favorite.objects.filter(member=self.member).count(), 0)

    def test_delete_not_favorited_is_404(self):
        self.assertEqual(self.client.delete(f"/api/v1/favorites/{self.product.id}/").status_code, 404)

    def test_requires_login(self):
        self.assertEqual(auth_client().get("/api/v1/favorites/").status_code, 401)
