# from datetime import timedelta
# from django.test import TestCase, override_settings
# from django.core import mail
# from django.conf import settings
# from django.utils import timezone

# from ..components.task_notification import send_task_notification, send_overdue_task_reminders
# from ..models.email_notification_model import EmailNotification
# from ..models.task_models import Task
# from ..models.user_models import User
# from ..models.role_models import Role  

# @override_settings(
#     EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
#     DEFAULT_FROM_EMAIL='from@example.com'
# )
# class EmailNotificationTaskTests(TestCase):
#     def setUp(self):
#         # Create a dummy role and assign it to the user.
#         self.role = Role.objects.create(name="user")  # Adjust fields as necessary
#         self.user = User.objects.create(
#             email='test@example.com',
#             full_name="Test User",
#             password="testpass",
#             role=self.role
#         )
        
#         self.task = Task.objects.create(
#             assigner=self.user,
#             assignee=self.user,
#             category_id=1,  # Use an existing category id or create one if needed.
#             name='Test Task',
#             status='not_started',
#             priority='high',
#             due_date=timezone.now() + timedelta(days=1),
#             start_date=timezone.now(),
#             end_date=timezone.now() + timedelta(days=1),
#             description='Test description'
#         )
    
#     def test_send_task_notification(self):
#         """
#         Test that send_task_notification sends an email for a new task notification
#         and marks the notification as sent.
#         """
#         notification = EmailNotification.objects.create(
#             user=self.user,
#             task=self.task,
#             message="You have been assigned a new task: Test Task",
#             is_sent=False
#         )
        
#         mail.outbox = []
        
#         send_task_notification(notification.id)
        
#         notification.refresh_from_db()
        
#         self.assertEqual(len(mail.outbox), 1)
#         email = mail.outbox[0]
#         self.assertEqual(email.subject, "New Task Assigned")
#         self.assertIn(notification.message, email.body)
#         self.assertIn(self.task.name, email.body)
#         self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
#         self.assertEqual(email.to, [self.user.email])
        
#         self.assertTrue(notification.is_sent)
    
#     def test_send_overdue_task_reminders(self):
#         """
#         Test that send_overdue_task_reminders creates a notification (if needed),
#         sends a reminder email, and marks the notification as sent.
#         """
#         self.task.due_date = timezone.now() - timedelta(days=1)
#         self.task.status = 'pending'
#         self.task.save()
        
#         EmailNotification.objects.all().delete()
#         mail.outbox = []
        
#         send_overdue_task_reminders()
        
#         notification = EmailNotification.objects.filter(task=self.task, user=self.user).first()
#         self.assertIsNotNone(notification)
#         self.assertTrue(notification.is_sent)
        
#         self.assertGreater(len(mail.outbox), 0)
#         email = mail.outbox[0]
#         self.assertEqual(email.subject, "Task Overdue Reminder")
#         self.assertIn("overdue", email.body.lower())
#         self.assertEqual(email.from_email, settings.DEFAULT_FROM_EMAIL)
#         self.assertEqual(email.to, [self.user.email])
