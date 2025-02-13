from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

from ..mixins.mixins import BaseModelMixin
from .user_models import User
import logging

logger = logging.getLogger(__name__)

class Task(BaseModelMixin):  # id, created_at, updated_at
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = '_task'
        ordering = ['-created_at']
    
    class PriorityChoices(models.Choices):
        VERY_HIGH = "very_high"
        HIGH = "high"
        MEDIUM = "medium"
        LOW = "low"

    class StatusChoices(models.Choices):
        COMPLETED = "completed"
        IN_PROGRESS = "in_progress"
        PENDING = "pending"
        NOT_STARTED ="not_started"

    assigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")  
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_tasks")
    name = models.CharField(max_length=255, default="No name")
    status = models.CharField(max_length=11, choices=StatusChoices.choices, default=StatusChoices.NOT_STARTED)
    priority = models.CharField(max_length=11, choices=PriorityChoices.choices, default=PriorityChoices.HIGH)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(default=now)
    description = models.TextField(max_length=1000, default="No description")


    def __str__(self):
        return f"{self.name} (Assigned to: {self.user.username})"

    def clean(self):
        """Validate task before saving."""
        if not self.start_date or not self.end_date:
            if self.status == "completed":
                raise ValidationError("Cannot set status completed while theres no full dates.")

        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date.")

        conflict_exists = Task.objects.filter(
            user=self.user,
            completed=False,
            start_date__lt=self.end_date,  
            end_date__gt=self.start_date
        ).exclude(id=self.id).exists()

        if conflict_exists:
            raise ValidationError("Time conflict: This task overlaps with another active task.")

    def save(self, *args, **kwargs):
        """Ensure task is valid before saving."""
        try:
            self.clean()  
            super().save(*args, **kwargs)
            logger.info(f"Task '{self.name}' saved successfully for user {self.user.username}")
        except ValidationError as e:
            logger.error(f"Task '{self.name}' could not be saved: {e}")
            raise
    