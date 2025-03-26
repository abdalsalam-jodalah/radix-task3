from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from .user_models import User
from .task_models import Task
import logging

logger = logging.getLogger(__name__)

class EmailNotification(models.Model):
    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        db_table = '_email_notification'
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="notifications")
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.task.name}"

    def validate_message(self):
        if not self.message or not self.message.strip():
            raise ValidationError({"message": "Message cannot be empty."})

    def clean(self):
        super().clean()
        self.validate_message()

    def save(self, *args, **kwargs):
        self.full_clean()  
        logger.info(f"Saving notification for user '{self.user.email}' regarding task '{self.task.name}'")
        super().save(*args, **kwargs)
