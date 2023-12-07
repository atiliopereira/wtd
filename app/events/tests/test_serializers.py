from django.test import TestCase
from model_bakery import baker

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
            date="2021-01-01T00:00:00Z",
            location="Test Location",
        )
        self.event.tags.add(self.tag)

    def test_tag_serializer(self):
        serializer = TagSerializer(self.tag)
        self.assertEqual(
            serializer.message.name, "Test Tag"
        )
    
    def test_event_serializer(self):
        new_tag = baker.make(models.Tag, name="New Tag")
        self.event.tags.add(new_tag)
        serializer = EventSerializer(self.event)
        
        self.assertEqual(serializer.message.title, "Test Event")
        self.assertEqual(serializer.message.description, "Test Description")
        self.assertEqual(serializer.message.date, "2021-01-01T00:00:00Z")
        self.assertEqual(serializer.message.location, "Test Location")
        self.assertEqual(serializer.message.status, 1) # Pending = 1
        self.assertEqual(len(serializer.message.tags), 2)
        self.assertEqual(serializer.message.tags[0].name, "Test Tag")
        self.assertEqual(serializer.message.tags[1].name, "New Tag")


