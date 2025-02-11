from django.urls import path
from ..controllers.task_controllers import TaskApi

urlpatterns = [
    path('task/', TaskApi.as_view(), name='task-crud'),
    path('task/<uuid:pk>/', TaskApi.as_view(), name='task-id-crud'),
]