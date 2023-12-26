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
        read_only_fields = ("id", "created_at", "updated_at")

    def create(self, validated_data):
        tags = validated_data.pop("tags")
        event = Event.objects.create(**validated_data)
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(**tag)
            event.tags.add(tag)
        return event

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.date = validated_data.get("date", instance.date)
        instance.location = validated_data.get("location", instance.location)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        instance.tags.clear()

        tags = validated_data.pop("tags")
        for tag in tags:
            tag, _ = Tag.objects.get_or_create(**tag)
            instance.tags.add(tag)
        return instance
