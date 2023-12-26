from rest_framework.routers import DefaultRouter

from app.events.views import EventViewSet

v1_router = DefaultRouter()
v1_router.register(r"events", EventViewSet)

v1_urls = v1_router.urls
