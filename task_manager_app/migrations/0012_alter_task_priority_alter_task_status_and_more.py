# Generated by Django 5.1.6 on 2025-02-28 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_manager_app", "0011_alter_task_priority_alter_task_status_and_more"),
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
            model_name="userdevice",
            name="device_token",
            field=models.CharField(
                default="BvdvwzDbFiZxGe3gcNj28NhUyn4r0ZIlq2NDJWZg2LI3Ug1del6y4wsApXTEW2We",
                max_length=255,
                unique=True,
            ),
        ),
    ]
