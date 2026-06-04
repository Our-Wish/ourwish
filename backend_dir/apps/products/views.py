from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductDetailSerializer


# Create your views here.
class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        product = get_object_or_404(
            Product.objects.select_related("bank").prefetch_related(
                "options", "conditions"
            ),
            id=product_id,
        )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)
