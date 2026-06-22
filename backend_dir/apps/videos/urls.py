from django.urls import path

from .views import VideoDetailView, VideoSearchView

urlpatterns = [
    # GET(검색) — ?q=키워드. '<video_id>'보다 위에 둬야 'search'가 영상ID로 안 잡힘
    path("search/", VideoSearchView.as_view(), name="video_search"),
    # GET(상세) — YouTube videoId로 식별
    path("<str:video_id>/", VideoDetailView.as_view(), name="video_detail"),
]
