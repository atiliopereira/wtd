from rest_framework import serializers

from app.events.models import Event, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]


class EventSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "date",
            "location",
            "status",
            "created_at",
            "updated_at",
            "tags",
        )
