from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="FPSO API",
      default_version='v1',
      description="",
      terms_of_service="",
      contact=openapi.Contact(email="diegoreis@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^docs/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]