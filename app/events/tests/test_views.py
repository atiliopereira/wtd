import datetime

from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIRequestFactory

from app.events import models
from app.events.serializers import EventSerializer
from app.events.views import EventViewSet


class TestEventViewSet(TestCase):
    def setUp(self):
        self.view = EventViewSet()
        self.connector = baker.make(models.Connector, source_type=models.Connector.MANUAL)
        self.event = baker.make(
            models.Event,
            title="Test Event",
            description="Test Description",
            category=models.Event.CONCERT,
            start=datetime.datetime(2024, 1, 1, 20, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2024, 1, 1, 23, 0, tzinfo=datetime.timezone.utc),
            venue_name="Test Venue",
            city="Madrid",
            is_free=False,
            price_info="From €15",
            status=models.Event.PUBLISHED,
            source_type=models.Connector.MANUAL,
            source_connector=self.connector,
        )
        self.request_factory = APIRequestFactory()

    def test_get_queryset(self):
        self.assertIn(self.event, self.view.get_queryset())

    def test_get_serializer_class(self):
        self.assertEqual(self.view.get_serializer_class(), EventSerializer)

    def test_post_create_event(self):
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
        request = self.request_factory.post("/api/v1/events/", data, format="json")
        request.data = data
        self.view.request = request
        self.view.format_kwarg = "json"
        response = self.view.create(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(models.Event.objects.filter(title="New Event").count(), 1)

    def test_get_retrieve_event(self):
        request = self.request_factory.get("/api/v1/events/", format="json")
        self.view.request = request
        self.view.format_kwarg = "json"
        self.view.kwargs = {"pk": self.event.id}
        response = self.view.retrieve(request, pk=self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Event")
        self.assertEqual(response.data["city"], "Madrid")

    def test_put_update_event(self):
        data = {
            "title": "Updated Event",
            "description": "Updated description",
            "category": models.Event.FESTIVAL,
            "start": "2024-06-01T20:00:00Z",
            "venue_name": "New Venue",
            "city": "Barcelona",
            "is_free": False,
            "price_info": "From €25",
            "status": models.Event.PUBLISHED,
        }
        request = self.request_factory.put("/api/v1/events/", data, format="json")
        request.data = data
        self.view.request = request
        self.view.format_kwarg = "json"
        self.view.kwargs = {"pk": self.event.id}
        response = self.view.update(request, pk=self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(models.Event.objects.filter(title="Updated Event").count(), 1)

    def test_get_list_events(self):
        for i in range(5):
            baker.make(
                models.Event,
                title=f"Event {i}",
                start=datetime.datetime(2024, 1, 1, 20, 0, tzinfo=datetime.timezone.utc),
                venue_name="Venue",
                city="Madrid",
                is_free=True,
            )
        request = self.request_factory.get("/api/v1/events/", format="json")
        self.view.request = request
        self.view.format_kwarg = "json"
        response = self.view.list(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)
