from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from U2_rest import settings

schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Test description",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path(
        'api/v1/', include(
            [
                path('task/', include('task_manager.urls')),
                path('accounts/', include('accounts.urls')),
                path('notification/', include('notification.urls')),

            ]
        )
    )
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
