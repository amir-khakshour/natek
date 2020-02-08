from rest_framework import generics
from goods.models import Product
from .serializers import ProductSerializer


class ProductViewSet(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
