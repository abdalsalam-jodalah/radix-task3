import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "authApi.settings")

app = Celery("authApi")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-overdue-reminders-daily": {
        "task": "your_app.tasks.send_overdue_task_reminders",  
        # "schedule": crontab(hour=15, minute=0), 
        "schedule": 600, 
    },
}
