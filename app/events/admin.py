from django.contrib import admin
from app.events.models import Event, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
    fields = ("name",)
    readonly_fields = ("id",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "start", "end", "location", "status",)
    list_filter = ("status",)
    search_fields = (
        "id",
        "title",
        "description",
    )
    fields = (
        "title",
        "description",
        "start",
        "end",
        "location",
        "status",
        "tags",
    )
    readonly_fields = ("id", "status", "tags", "created_at", "updated_at")
