# Generated by Django 5.1.6 on 2025-03-25 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "task_manager_app",
            "0022_alter_task_id_alter_task_priority_alter_task_status_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="id",
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
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
            model_name="userdevice",
            name="device_token",
            field=models.CharField(
                default="VDBV45i5C08j9WGkqTYsJHbjUhgqMyIJIU2KbfmQ7MkiGR6Q1RB30OxnA3S05ALl",
                max_length=255,
                unique=True,
            ),
        ),
    ]
