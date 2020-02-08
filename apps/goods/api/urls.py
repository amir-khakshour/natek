from django.urls import path, include
from rest_framework import routers

from .views import (
    ProductViewSet,
)

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]

print("urlpatterns", urlpatterns)
