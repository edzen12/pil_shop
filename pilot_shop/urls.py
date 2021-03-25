from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import api_root


schema_view = get_schema_view(
    openapi.Info(
        title = "Shop API",
        default_version = 'v1',
        description = "Simple e-commerce API documentation",
        terms_of_service = "https://policies.google.com/terms",
        license = openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),

    path('admin/', admin.site.urls),
    path('api/', api_root, name='api_root'),
    path('api/products/', include('apps.products.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api_auth/', include('rest_framework.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/carts/', include('apps.carts.urls')),
    path('api/orders/', include('apps.orders.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
