from django.db import models

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