from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

from ..mixins.mixins import BaseModelMixin
from .user_models import User

import logging
logger = logging.getLogger("models")

class Task(BaseModelMixin): #id, created_at, updated_at
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        db_table = '_task'
        ordering = ['-created_at']

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")  # Fixed relationship
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=1000)
    completed = models.BooleanField(default=False)
    start_date = models.DateTimeField(default=datetime.now)
    end_date = models.DateTimeField(default=datetime.now)  

    def __str__(self):
        return f"{self.name} from {self.from_user} to {self.to_user}"

    def save(self, *args, **kwargs):
        self.validate_task_dates() # i feel like i should keep clean method and call validate_task_dates inside it since it validation related 
        self.clean()  
        super().save(*args, **kwargs)
    
    def validate_task_dates(self):   
        if self.start_date >= self.end_date:
            raise ValidationError("Start date should be before end date.")
        
        user_tasks = Task.objects.filter(
            user=self.user,
            completed=False  
        ).exclude(id=self.id) 
        
        for task in user_tasks:
            if not (self.end_date <= task.start_date or self.start_date >= task.end_date):
                raise ValidationError("Time conflict: This task conflicts with another task.")