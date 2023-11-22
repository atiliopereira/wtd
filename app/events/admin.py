from django.contrib import admin
from app.events.models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "location", "status")
    list_filter = ("status",)
    search_fields = (
        "id",
        "title",
        "description",
    )
    fields = (
        "title",
        "description",
        "date",
        "location",
        "status",
    )
    readonly_fields = ("id", "status", "created_at", "updated_at")
