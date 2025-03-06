from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from ..models.email_notification_model import EmailNotification
from django.utils.timezone import now
from ..models.task_models import Task

@shared_task
def send_task_notification(notification_id):
    notification = EmailNotification.objects.get(id=notification_id)
    
    if not notification.is_sent:
        subject = "New Task Assigned"
        message = f"{notification.message}\nTitle: {notification.task.name}\n\nTask Details:{notification.task}\n\n\n Task Manager app team..."
        recipient_email = notification.user.email

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )

        notification.is_sent = True
        notification.save()

@shared_task
def send_overdue_task_reminders():
    overdue_tasks = Task.objects.filter(due_date__lt=now(), status__in=['pending', 'in_progress'])

    notifications_to_create = []
    emails_to_send = []

    for task in overdue_tasks:
        notification, created = EmailNotification.objects.get_or_create(
            user=task.assignee,
            task=task,
            defaults={'message': f"Your task '{task.name}' is overdue! Please complete it ASAP."},
        )

        if not notification.is_sent:
            emails_to_send.append({
                "subject": "Task Overdue Reminder",
                "message": notification.message,
                "recipient": task.assignee.email,
            })
            notifications_to_create.append(notification)

    for email in emails_to_send:
        send_mail(
            subject=email["subject"],
            message=email["message"],
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email["recipient"]],
            fail_silently=True,
        )

    EmailNotification.objects.filter(id__in=[n.id for n in notifications_to_create]).update(is_sent=True)