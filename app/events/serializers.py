from django_grpc_framework import proto_serializers

from app.events.models import Event, Tag
from app.events.protobuf import events_pb2


class TagSerializer(proto_serializers.ModelProtoSerializer):
    class Meta:
        model = Tag
        proto_class = events_pb2.Tag
        fields = ["name"]


class EventSerializer(proto_serializers.ModelProtoSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Event
        proto_class = events_pb2.Event
        fields = [
            "id",
            "title",
            "description",
            "date",
            "location",
            "status",
            "tags",
        ]
        read_only_fields = ["id", "status", "tags"]
