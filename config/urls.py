from django.contrib import admin
from django.urls import path, register_converter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

from .utils import ApiConverter

register_converter(ApiConverter, 'api')

urlpatterns = [
    path('admin/', admin.site.urls),
]

# JWT token
urlpatterns += [
    path('<api:version>/api-token-auth/', obtain_jwt_token),
    path('<api:version>/api-token-refresh/', refresh_jwt_token),
]
