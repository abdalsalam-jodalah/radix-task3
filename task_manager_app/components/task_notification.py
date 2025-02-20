from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from ..models.email_notification_model import EmailNotification

@shared_task
def send_task_notification(notification_id):
    notification = EmailNotification.objects.get(id=notification_id)
    
    if not notification.is_sent:
        subject = "New Task Assigned"
        message = f"{notification.message}\n\nTask Details:\nTitle: {notification.task.name}"
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
