from django.urls import path

from .views import ProductChatView, ProductDetailView, ProductRecommendView

urlpatterns = [
    path("recommend/", ProductRecommendView.as_view(), name="product_recommend"),
    path("<int:product_id>/chat/", ProductChatView.as_view(), name="product_chat"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
]
