from django.contrib import admin
from django.utils import timezone

from app.events.models import Connector, Event


@admin.register(Connector)
class ConnectorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "source_type", "is_active", "last_run_at", "consecutive_failures")
    list_filter = ("source_type", "is_active")
    search_fields = ("id", "name")
    fields = ("name", "source_type", "config", "is_active")
    readonly_fields = ("id", "last_run_at", "last_error", "consecutive_failures", "created_at", "updated_at")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "start", "venue_name", "city", "is_free", "status", "confirmed")
    list_filter = ("status", "category", "is_free", "confirmed", "source_type")
    search_fields = ("id", "title", "description", "venue_name", "city")
    readonly_fields = ("id", "confirmed", "confirmed_by", "confirmed_at", "source_type", "source_connector", "external_id", "created_at", "updated_at")
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
        "status",
        "confirmed",
        "confirmed_by",
        "confirmed_at",
        "source_type",
        "source_url",
        "source_connector",
        "external_id",
        "created_at",
        "updated_at",
    )
    actions = ["confirm_events", "publish_events", "reject_events"]

    @admin.action(description="Confirm selected events")
    def confirm_events(self, request, queryset):
        queryset.update(confirmed=True, confirmed_by=request.user, confirmed_at=timezone.now())

    @admin.action(description="Publish selected events")
    def publish_events(self, request, queryset):
        queryset.update(status=Event.PUBLISHED)

    @admin.action(description="Reject selected events")
    def reject_events(self, request, queryset):
        queryset.update(status=Event.REJECTED)
