from django.urls import path
from ..controllers.task_controllers import TaskApi, ByUser

urlpatterns = [
    path('task/',           TaskApi.as_view(), name='task-crud'),
    path('task/<uuid:pk>/', TaskApi.as_view(), name='task-id-crud'),
    path('task/byuser/',        ByUser.as_view(), name='task-id-crud'),
    path('task/',        ByUser.as_view(), name='task-id-crud'),
    
]