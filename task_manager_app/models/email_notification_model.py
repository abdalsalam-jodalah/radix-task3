from django.db import models
from django.utils.timezone import now
from .user_models import User
from .task_models import Task

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
