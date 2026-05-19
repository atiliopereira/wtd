from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from app.events.models import Connector, Event
from app.events.serializers import ConnectorSerializer, EventSerializer


@extend_schema(responses=EventSerializer)
class EventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Event.objects.select_related("source_connector", "confirmed_by").all()
    serializer_class = EventSerializer
    ordering_fields = ("created_at", "updated_at", "id", "start")
    ordering = ("-start",)
    filterset_fields = ("status", "category", "is_free", "confirmed", "city")


@extend_schema(responses=ConnectorSerializer)
class ConnectorViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Connector.objects.all()
    serializer_class = ConnectorSerializer
    ordering_fields = ("created_at", "updated_at", "id")
    ordering = ("-created_at",)
