from rest_framework import serializers

from app.events.models import Connector, Event


class ConnectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connector
        fields = (
            "id",
            "name",
            "source_type",
            "config",
            "is_active",
            "last_run_at",
            "last_error",
            "consecutive_failures",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "last_run_at", "last_error", "consecutive_failures", "created_at", "updated_at")


class EventSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    end = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", allow_null=True, required=False)
    confirmed_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "category",
            "start",
            "end",
            "venue_name",
            "venue_address",
            "city",
            "is_free",
            "price_info",
            "ticket_url",
            "image_url",
            "source_type",
            "source_url",
            "source_connector",
            "external_id",
            "status",
            "confirmed",
            "confirmed_by",
            "confirmed_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "confirmed",
            "confirmed_by",
            "confirmed_at",
            "created_at",
            "updated_at",
        )
