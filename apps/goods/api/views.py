import contextlib
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Brand, Category, Product
from ..drf.views import ReadWriteSerializerMixin
from .serializers import BrandSerializer, CategorySerializer, ProductReadSerializer, ProductWriteSerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


@contextlib.contextmanager
def override_serializer(view, serializer):
    orig_serializer_class = view.serializer_class
    view.serializer_class = serializer
    yield serializer
    view.serializer_class = orig_serializer_class


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk, version=None):
        products = Product.objects.filter(categories__id=pk)
        page = self.paginate_queryset(products)
        with override_serializer(self, ProductReadSerializer):
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(ReadWriteSerializerMixin, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    read_serializer_class = ProductReadSerializer
    write_serializer_class = ProductWriteSerializer

    def perform_create(self, serializer):
        """
        override some readonly fields
        :param serializer:
        :return:
        """
        override_fields = {
            'created_by': self.request.user
        }
        serializer.save(**override_fields)
