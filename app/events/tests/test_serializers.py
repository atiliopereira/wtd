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

    def test_event_serializer_create_with_existing_tag(self):
        data = {
            "title": "Test Event Create",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "Test Tag"}],
        }
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Create").count(),
            1,
        )

    def test_event_serializer_create_create_tag(self):
        data = {
            "title": "Test Event Create Create Tag",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "New Tag"}],
        }
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Create Create Tag").count(),
            1,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            1,
        )

    def test_event_serializer_update(self):
        data = {
            "title": "Test Event Update",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "Test Tag"}],
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Update").count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.filter(title="Test Event").count(),
            0,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="Test Tag").count(),
            1,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            0,
        )

    def test_event_serializer_update_create_tag(self):
        data = {
            "title": "Test Event Update Create Tag",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "New Tag"}],
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Update Create Tag").count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.filter(title="Test Event").count(),
            0,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            1,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="Test Tag").count(),
            1,
        )

    def test_event_serializer_update_remove_tag(self):
        data = {
            "title": "Test Event Update Remove Tag",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [],
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Update Remove Tag").count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.filter(title="Test Event").count(),
            0,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            0,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="Test Tag").count(),
            1,
        )

    def test_event_serializer_update_remove_tag_add_new_tag(self):
        data = {
            "title": "Test Event Update Remove Tag Add New Tag",
            "description": "Test Description",
            "date": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "New Tag"}, {"name": "Test Tag"}],
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.assertEqual(
            models.Event.objects.filter(
                title="Test Event Update Remove Tag Add New Tag"
            ).count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.filter(title="Test Event").count(),
            0,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            1,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="Test Tag").count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.get(
                title="Test Event Update Remove Tag Add New Tag"
            ).tags.count(),
            2,
        )
