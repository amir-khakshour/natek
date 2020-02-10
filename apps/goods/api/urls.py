from django.urls import path, include
from rest_framework import routers

from .views import (
    ProductViewSet,
    BrandViewSet,
    CategoryViewSet
)

app_name = 'api_goods'
router = routers.DefaultRouter()
router.register(r'brand', BrandViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'product', ProductViewSet)

urlpatterns = router.urls
