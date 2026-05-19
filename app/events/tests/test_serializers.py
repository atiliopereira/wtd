import datetime

from django.test import TestCase
from model_bakery import baker

from app.common.utils import datetime_to_drf_str
from app.events import models
from app.events.serializers import EventSerializer


class TestEventSerializer(TestCase):
    def setUp(self):
        self.connector = baker.make(models.Connector, source_type=models.Connector.MANUAL)
        self.event = baker.make(
            models.Event,
            title="Test Event",
            description="Test Description",
            category=models.Event.CONCERT,
            start=datetime.datetime(2024, 1, 1, 20, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2024, 1, 1, 23, 0, tzinfo=datetime.timezone.utc),
            venue_name="Test Venue",
            venue_address="123 Main St",
            city="Madrid",
            is_free=False,
            price_info="From €15",
            ticket_url="https://example.com/tickets",
            source_type=models.Connector.MANUAL,
            source_connector=self.connector,
            status=models.Event.PUBLISHED,
        )

    def test_event_serializer_fields(self):
        serializer = EventSerializer(self.event)
        data = serializer.data

        self.assertEqual(data["title"], self.event.title)
        self.assertEqual(data["description"], self.event.description)
        self.assertEqual(data["category"], models.Event.CONCERT)
        self.assertEqual(data["start"], datetime_to_drf_str(self.event.start))
        self.assertEqual(data["end"], datetime_to_drf_str(self.event.end))
        self.assertEqual(data["venue_name"], self.event.venue_name)
        self.assertEqual(data["city"], self.event.city)
        self.assertEqual(data["is_free"], False)
        self.assertEqual(data["price_info"], "From €15")
        self.assertEqual(data["status"], models.Event.PUBLISHED)
        self.assertEqual(data["confirmed"], False)

    def test_event_serializer_create(self):
        data = {
            "title": "New Event",
            "description": "A description",
            "category": models.Event.PARTY,
            "start": "2024-06-01T20:00:00Z",
            "venue_name": "Some Club",
            "city": "Madrid",
            "is_free": True,
            "status": models.Event.PUBLISHED,
        }
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()

        self.assertEqual(models.Event.objects.filter(title="New Event").count(), 1)
        self.assertEqual(event.is_free, True)
        self.assertEqual(event.city, "Madrid")

    def test_event_serializer_update(self):
        data = {
            "title": "Updated Event",
            "description": "Updated description",
            "category": models.Event.FESTIVAL,
            "start": "2024-06-01T20:00:00Z",
            "venue_name": "New Venue",
            "city": "Barcelona",
            "is_free": False,
            "price_info": "From €20",
            "status": models.Event.PUBLISHED,
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.event.refresh_from_db()
        self.assertEqual(self.event.title, "Updated Event")
        self.assertEqual(self.event.city, "Barcelona")
        self.assertEqual(self.event.price_info, "From €20")

    def test_confirmed_fields_are_read_only(self):
        data = {
            "title": "Test Event",
            "start": "2024-06-01T20:00:00Z",
            "venue_name": "Venue",
            "city": "Madrid",
            "is_free": True,
            "confirmed": True,
        }
        serializer = EventSerializer(self.event, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        self.event.refresh_from_db()
        self.assertEqual(self.event.confirmed, False)

    def test_free_event_has_no_price_info(self):
        data = {
            "title": "Free Event",
            "start": "2024-06-01T20:00:00Z",
            "venue_name": "Park",
            "city": "Madrid",
            "is_free": True,
            "status": models.Event.PUBLISHED,
        }
        serializer = EventSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        event = serializer.save()
        self.assertEqual(event.price_info, "")
