from django.urls import path

from .views import ProductDetailView, ProductRecommendView

urlpatterns = [
    path("recommend/", ProductRecommendView.as_view(), name="product_recommend"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="product_detail"),
]
