# Generated by Django 5.0.3 on 2024-03-07 13:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="booked",
                to="booking.room",
                unique=True,
            ),
        ),
    ]
