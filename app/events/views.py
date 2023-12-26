from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from app.events.models import Event
from app.events.serializers import EventSerializer


@extend_schema(responses=EventSerializer)
class EventViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    ordering_fields = (
        "created_at",
        "updated_at",
        "id",
    )
    ordering = ("-created_at",)
