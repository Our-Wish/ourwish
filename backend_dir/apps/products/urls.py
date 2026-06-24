from django.urls import path

from .views import (
    MarketRateView,
    ProductChatView,
    ProductDetailView,
    ProductRecommendView,
)

urlpatterns = [
    path("recommend/", ProductRecommendView.as_view(), name="product_recommend"),
    # STEP1 평균 금리 — '<int:product_id>'보다 위에 둔다(문자열이라 충돌은 없지만 명시)
    path("market-rates/", MarketRateView.as_view(), name="market_rates"),
    path("<int:product_id>/chat/", ProductChatView.as_view(), name="product_chat"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
]
