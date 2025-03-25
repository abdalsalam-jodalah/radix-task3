from django.urls import path
from ..controllers.task_controllers import TaskApi, TaskApiByUser

urlpatterns = [
    path('task/',           TaskApi.as_view(), name='task-crud'),
    path('task/<int:id>/', TaskApi.as_view(), name='task-id-crud'),
    
    path('task/byuser/',            TaskApiByUser.as_view(), name='task-byuser-crud'),
    path('task/byuser/<int:id>',   TaskApiByUser.as_view(), name='task-byuser-id-crud'),
    
]