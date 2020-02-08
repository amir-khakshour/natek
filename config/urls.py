from django.conf import settings
from django.contrib import admin
from django.urls import path, register_converter, include
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

# Goods app
urlpatterns += [
    path('<api:version>/goods/', include('goods.api.urls'))
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
