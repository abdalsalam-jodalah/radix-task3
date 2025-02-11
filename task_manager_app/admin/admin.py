from django.contrib import admin
from django.contrib.auth import get_user_model
from ..models.task_models import Task
from ..models.user_models import UserDevice

User = get_user_model()
admin.site.register(User)
admin.site.register(Task)
admin.site.register(UserDevice)
