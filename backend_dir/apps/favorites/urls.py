from django.urls import path

from .views import FavoriteDeleteView, FavoriteListCreateView

urlpatterns = [
    # GET(목록) + POST(찜 추가)
    path("", FavoriteListCreateView.as_view(), name="favorite_list_create"),
    # DELETE(찜 해제) — product_id로 식별
    path("<int:product_id>/", FavoriteDeleteView.as_view(), name="favorite_delete"),
]
