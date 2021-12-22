"""channels_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenRefreshView

from channels_test import settings
from chat.views import Login

schema_view = get_schema_view(
    openapi.Info(
        title="Honors",
        default_version='v1',
        # description="Test description",

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/chat/', include('chat.urls')),
    path('api/admin/', admin.site.urls),
    path('api/login/', Login.as_view(), name='login'),
    path('api/refresh/', TokenRefreshView.as_view(), name='refresh'),
]

urlpatterns += [path('api/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)