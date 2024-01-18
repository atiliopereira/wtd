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
        self.tag = baker.make(
            models.Tag,
            name="Test Tag",
        )
        self.event = baker.make(
            models.Event,
            title="Test Event",
            description="Test Description",
            start=datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
            end=datetime.datetime(2024, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
            location="Test Location",
        )
        self.event.tags.add(self.tag)
        self.request_factory = APIRequestFactory()

    def test_get_queryset(self):
        self.assertEqual(
            list(self.view.get_queryset()),
            [self.event],
        )

    def test_get_serializer_class(self):
        self.assertEqual(self.view.get_serializer_class(), EventSerializer)

    def test_post_create_event(self):
        data = {
            "title": "Test Event Create",
            "description": "Test Description",
            "start": "2024-01-01T00:00:00Z",
            "end": "2024-01-01T00:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "Test Tag"}],
        }
        request = self.request_factory.post(
            "/api/v1/events/",
            data,
            format="json",
        )
        request.data = data
        self.view.request = request
        self.view.format_kwarg = "json"
        response = self.view.create(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Create").count(),
            1,
        )

    def test_get_retrieve_event(self):
        request = self.request_factory.get(
            "/api/v1/events/",
            format="json",
        )
        self.view.request = request
        self.view.format_kwarg = "json"
        self.view.kwargs = {"pk": self.event.id}
        response = self.view.retrieve(request, pk=self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Event")

    def test_put_update_event(self):
        data = {
            "title": "Test Event Updated",
            "description": "Test Description",
            "start": "2024-01-01T00:00:00Z",
            "end": "2024-01-01T01:00:00Z",
            "location": "Test Location",
            "tags": [{"name": "Test Tag"}, {"name": "New Tag"}],
        }
        request = self.request_factory.put(
            "/api/v1/events/",
            data,
            format="json",
        )
        request.data = data
        self.view.request = request
        self.view.format_kwarg = "json"
        self.view.kwargs = {"pk": self.event.id}
        response = self.view.update(request, pk=self.event.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            models.Event.objects.filter(title="Test Event Updated").count(),
            1,
        )
        self.assertEqual(
            models.Tag.objects.filter(name="New Tag").count(),
            1,
        )
        self.assertEqual(
            models.Event.objects.get(title="Test Event Updated").tags.count(),
            2,
        )

    def test_get_list_events(self):
        for i in range(5):
            event_title = f"Test Event {i}"
            event = baker.make(
                models.Event,
                title=event_title,
                description="Test Description",
                start=datetime.datetime(2024, 1, 1, 0, 0, tzinfo=datetime.timezone.utc),
                end=datetime.datetime(2024, 1, 1, 1, 0, tzinfo=datetime.timezone.utc),
                location="Test Location",
            )
            event.tags.add(self.tag)

        request = self.request_factory.get(
            "/api/v1/events/",
            format="json",
        )
        self.view.request = request
        self.view.format_kwarg = "json"
        response = self.view.list(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 6)
        self.assertEqual(response.data[0]["title"], "Test Event")
        self.assertEqual(response.data[1]["title"], "Test Event 0")
        self.assertEqual(response.data[2]["title"], "Test Event 1")
        self.assertEqual(response.data[3]["title"], "Test Event 2")
        self.assertEqual(response.data[4]["title"], "Test Event 3")
        self.assertEqual(response.data[5]["title"], "Test Event 4")
