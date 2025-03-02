# Generated by Django 5.1.6 on 2025-02-27 07:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager_app", "0006_permission_access_level_permission_action_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="due_date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="task",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="priority",
            field=models.CharField(
                choices=[
                    ("very_high", "Very High"),
                    ("high", "High"),
                    ("medium", "Medium"),
                    ("low", "Low"),
                ],
                db_index=True,
                default="high",
                max_length=11,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="status",
            field=models.CharField(
                choices=[
                    ("completed", "Completed"),
                    ("in_progress", "In Progress"),
                    ("pending", "Pending"),
                    ("not_started", "Not Started"),
                ],
                db_index=True,
                default="not_started",
                max_length=11,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="userdevice",
            name="device_token",
            field=models.CharField(
                default="et0zMrcIkyC3N9LS0p5Gn1ZdplCOHL93Wtwo5f8QbAqxPSJtpkvpBXqkjK2HtAbN",
                max_length=255,
                unique=True,
            ),
        ),
    ]
