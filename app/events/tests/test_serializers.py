import datetime

from django.test import TestCase
from model_bakery import baker

from app.common.utils import datetime_to_drf_str
from app.events import models
from app.events.serializers import EventSerializer, TagSerializer


class TestSerializers(TestCase):
    def setUp(self):
        self.tag = baker.make(
            models.Tag,
            name="Test Tag",
        )
        self.event = baker.make(
            models.Event,
            title="Test Event",
            description="Test Description",
            date=datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            location="Test Location",
        )
        self.event.tags.add(self.tag)

    def test_tag_serializer(self):
        serializer = TagSerializer(self.tag)
        self.assertEqual(
            serializer.data,
            {
                "name": "Test Tag",
            },
        )

    def test_event_serializer(self):
        new_tag = baker.make(models.Tag, name="New Tag")
        self.event.tags.add(new_tag)
        serializer = EventSerializer(self.event)

        self.assertEqual(serializer.data["title"], self.event.title)
        self.assertEqual(serializer.data["description"], self.event.description)
        self.assertEqual(serializer.data["date"], datetime_to_drf_str(self.event.date))
        self.assertEqual(serializer.data["location"], self.event.location)
        self.assertEqual(serializer.data["status"], self.event.status)
        self.assertEqual(
            serializer.data["created_at"], datetime_to_drf_str(self.event.created_at)
        )
        self.assertEqual(
            serializer.data["updated_at"], datetime_to_drf_str(self.event.updated_at)
        )
        self.assertEqual(len(serializer.data["tags"]), 2)
        self.assertEqual(serializer.data["tags"][0]["name"], self.tag.name)
        self.assertEqual(serializer.data["tags"][1]["name"], new_tag.name)
