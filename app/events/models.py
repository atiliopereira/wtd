from django.contrib.auth.models import User
from django.db import models


class Connector(models.Model):
    MANUAL = "manual"
    API = "api"
    SCRAPER = "scraper"
    SOURCE_TYPES = (
        (MANUAL, "Manual"),
        (API, "API"),
        (SCRAPER, "Scraper"),
    )

    name = models.CharField(max_length=255)
    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    config = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True, default="")
    consecutive_failures = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.source_type})"


class Event(models.Model):
    CONCERT = "concert"
    THEATER = "theater"
    PARTY = "party"
    FESTIVAL = "festival"
    SPORT = "sport"
    EXHIBITION = "exhibition"
    OTHER = "other"
    CATEGORY_TYPES = (
        (CONCERT, "Concert"),
        (THEATER, "Theater"),
        (PARTY, "Party"),
        (FESTIVAL, "Festival"),
        (SPORT, "Sport"),
        (EXHIBITION, "Exhibition"),
        (OTHER, "Other"),
    )

    DRAFT = "draft"
    PUBLISHED = "published"
    REJECTED = "rejected"
    STATUS_TYPES = (
        (DRAFT, "Draft"),
        (PUBLISHED, "Published"),
        (REJECTED, "Rejected"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=20, choices=CATEGORY_TYPES, default=OTHER)
    start = models.DateTimeField()
    end = models.DateTimeField(null=True, blank=True)
    venue_name = models.CharField(max_length=255, default="")
    venue_address = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=255, default="")
    is_free = models.BooleanField(default=False)
    price_info = models.CharField(max_length=255, blank=True, default="")
    ticket_url = models.URLField(blank=True, default="")
    image_url = models.URLField(blank=True, default="")
    source_type = models.CharField(max_length=20, choices=Connector.SOURCE_TYPES, default=Connector.MANUAL)
    source_url = models.URLField(blank=True, default="")
    source_connector = models.ForeignKey(
        Connector, null=True, blank=True, on_delete=models.SET_NULL, related_name="events"
    )
    external_id = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default=DRAFT)
    confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="confirmed_events"
    )
    confirmed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["external_id", "source_connector"],
                condition=~models.Q(external_id=""),
                name="unique_external_id_per_connector",
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.start} ({self.status})"
