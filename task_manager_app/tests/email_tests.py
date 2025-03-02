from django.core import mail
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models.task_models import Task

User = get_user_model()

class TaskEmailNotificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="recipient", email="test@example.com", password="password")
        self.task = Task.objects.create(title="Email Task", assigned_to=self.user)

    def test_email_sent_on_task_assignment(self):
        mail.send_mail(
            subject="New Task Assigned",
            message=f"A new task '{self.task.title}' has been assigned to you.",
            from_email="noreply@taskapp.com",
            recipient_list=[self.user.email]
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "New Task Assigned")
