from django.db import models

class Event(models.Model):
    CANCELED = "Canceled"
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    STATUS_TYPES = (
        (CANCELED, "Canceled"),
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_TYPES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date} ({self.status})"

