from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.router import v1_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
    ),
    path("api/v1/", include((v1_urls, "router"), namespace="v1")),
]
