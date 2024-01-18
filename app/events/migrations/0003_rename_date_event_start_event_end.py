# Generated by Django 5.0 on 2023-12-29 19:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0002_tag_event_tags"),
    ]

    operations = [
        migrations.RenameField(
            model_name="event",
            old_name="date",
            new_name="start",
        ),
        migrations.AddField(
            model_name="event",
            name="end",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]