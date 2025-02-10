from django.urls import path
from ..controllers.task_controllers import TaskListView, TaskDetailView, TaskCreateView, TaskUpdateView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task-list'),
    path('tasks/<uuid:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('tasks/create/', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<uuid:pk>/update/', TaskUpdateView.as_view(), name='task-update'),
]
