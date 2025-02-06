from django.db import models
from authApi.mixins import BaseModelMixin
from services.user.models import User 

import logging
logger = logging.getLogger("models")

class Task(BaseModelMixin): #id, created_at, updated_at
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = 'user_tasks_table'
        ordering = ['-created_at']

    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    from_user= models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigner")
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "tasks")

    def __str__(self):
        return f"{self.name} from {self.from_user} to {self.to_user}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)