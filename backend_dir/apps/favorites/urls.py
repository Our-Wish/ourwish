from django.urls import path

from .views import (
    FavoriteDeleteView,
    FavoriteListCreateView,
    VideoFavoriteDeleteView,
    VideoFavoriteListCreateView,
)

urlpatterns = [
    # GET(목록) + POST(찜 추가)
    path("", FavoriteListCreateView.as_view(), name="favorite_list_create"),
    # 영상 찜 — '<int:product_id>'와 안 겹치게 위에 둔다.
    # GET(영상 찜 목록) + POST(영상 찜 등록)
    path(
        "videos/",
        VideoFavoriteListCreateView.as_view(),
        name="video_favorite_list_create",
    ),
    # DELETE(영상 찜 해제) — YouTube video_id로 식별
    path(
        "videos/<str:video_id>/",
        VideoFavoriteDeleteView.as_view(),
        name="video_favorite_delete",
    ),
    # DELETE(찜 해제) — product_id로 식별
    path("<int:product_id>/", FavoriteDeleteView.as_view(), name="favorite_delete"),
]
