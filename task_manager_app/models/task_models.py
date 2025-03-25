from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from ..constants.task_constants import PriorityChoices, StatusChoices
from ..mixins.mixins import BaseModelMixin
from .user_models import User
from .task_category_models import TaskCategory
import logging

logger = logging.getLogger(__name__)


class Task(BaseModelMixin):  # id, created_at, updated_at
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = '_task'
        ordering = ['-created_at']
    id = models.AutoField(editable=False, primary_key=True)
    assigner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_tasks")
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_tasks")
    category = models.ForeignKey(TaskCategory, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255, default="No name")
    status = models.CharField(max_length=11, choices=StatusChoices.choices, default=StatusChoices.NOT_STARTED, db_index=True)
    priority = models.CharField(max_length=11, choices=PriorityChoices.choices, default=PriorityChoices.HIGH, db_index=True)
    due_date = models.DateTimeField(default=now)
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField(default=now)
    description = models.TextField(max_length=1000, default="No description")

    def __str__(self):
        return f"{self.name} (Assigned to: {self.assignee.email})"
    def validate_dates(self):
        if self.due_date and self.due_date < now() :
            raise ValidationError({"due_date": "Cannot set due_date in the past."})
        
        if self.start_date and self.start_date < now() :
            raise ValidationError({"due_date": "Cannot set start_date in the past."})

    def validate_start_before_end(self):
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError({"start_before_end": "Start date must be before end date."})

    def validate_due_date_after_start(self):
        if self.start_date and self.due_date and self.due_date < self.start_date:
            raise ValidationError({"due_date_after_start": "Due date must be after the start date."})
        
    def validate_dates_and_completion(self):
        if (not self.start_date or not self.end_date) and self.status == StatusChoices.COMPLETED:
            raise ValidationError({"dates_and_completion": "Cannot set status completed while there are missing dates."})
        
    def validate_no_time_conflict(self):
        conflict_exists = Task.objects.filter(
            assignee=self.assignee,
            start_date__lt=self.end_date,
            due_date__gt=self.start_date
        ).exclude(id=self.id).exists()
        if conflict_exists:
            raise ValidationError({"time_conflict": "Time conflict: This task overlaps with another active task."})

    def clean(self):
        super().clean()
        self.validate_dates()
        self.validate_dates_and_completion()
        self.validate_start_before_end()
        self.validate_due_date_after_start()
        self.validate_no_time_conflict()

    def save(self, *args, **kwargs):
        self.full_clean()  
        logger.info(f"Saving Task '{self.name}' successfully for user {self.assignee.email}")
        super().save(*args, **kwargs)
