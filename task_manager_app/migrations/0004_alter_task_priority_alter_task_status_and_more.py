# Generated by Django 5.1.6 on 2025-02-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager_app", "0003_alter_task_priority_alter_task_status_and_more"),
    ]

    operations = [
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
                default="not_started",
                max_length=11,
            ),
        ),
        migrations.AlterField(
            model_name="userdevice",
            name="device_token",
            field=models.CharField(
                default="qwTXLEGFOHeob6sxdXiOzXXLGEmUq8ZBNCfA5cO2J3hF96iLAaTE4nA1xYuS1Nph",
                max_length=255,
                unique=True,
            ),
        ),
    ]
