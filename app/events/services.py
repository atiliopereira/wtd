from django_grpc_framework import generics
from app.events.serializers import EventSerializer
from app.events.models import Event


class EventService(generics.ModelService):
    """
    gRPC service that provides CRUD functions for Event model.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


