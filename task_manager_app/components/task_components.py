import datetime
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, ValidationError
from ..serializers.task_serializers import TaskSerializer
from ..repositories.task_repository import TaskRepository
from ..components.shared_components import SharedComponents as SC

class TaskComponents:
    def get_task_response(user, pk):
        task = TaskRepository.get_task_by_id(pk)
        if not task:
            return None, {"detail": "Task not found"}, 404
        if user.role != "admin" and task.user != user:
            raise PermissionDenied("You can only view your own tasks.")

        return task, TaskSerializer(task).data, 200

    def create_task(user, data):
        serializer = TaskSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            task = TaskRepository.create_task(user, serializer)
            return serializer.data, 201
        return None, {"detail": "Invalid data"}, 400

    def update_task(user, pk, data):
        task = TaskRepository.get_task_by_id(pk)
        if not task:
            return None, {"detail": "Task not found"}, 404

        if user.role != "admin" and task.user != user:
            raise PermissionDenied("You can only update your own tasks.")

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            TaskRepository.update_task(task, serializer)
            return serializer.data, 200
        return None, {"detail": "Invalid data"}, 400

    def delete_task(user, pk):
        task = TaskRepository.get_task_by_id(pk)
        if not task:
            return {"detail": "Task not found"}, 404

        if user.role != "admin" and task.user != user:
            raise PermissionDenied("You can only delete your own tasks.")

        TaskRepository.delete_task(task)
        return {"detail": "Task deleted successfully"}, 204
    
    def partial_update_task(user, pk, data):
        pass
    
    def get_tasks_assigned_by_user(user):
        tasks = TaskRepository.get_tasks_by_user(user).order_by('-created_at')
        if not tasks:
            return {"detail": "Tasks not found for this user"}, 404
        return tasks
    
    def get_tasks_filtered(user, filters=None, search_query=None):
        tasks = TaskRepository.get_tasks_for_user(user)
        if not tasks:
            return None, {"detail": "Tasks not found fro this user"}

        if search_query:
            tasks = tasks.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if filters:
            if 'priority' in filters:
                tasks = tasks.filter(priority=filters['priority'])
            
            if 'status' in filters:
                tasks = tasks.filter(status=filters['status'])

            if 'category' in filters:
                tasks = tasks.filter(category=filters['category'])

            if 'start_date' in filters and 'end_date' in filters:
                try:
                    start_date = datetime.strptime(filters['start_date'], "%Y-%m-%d")
                    end_date = datetime.strptime(filters['end_date'], "%Y-%m-%d")
                    tasks = tasks.filter(created_at__range=(start_date, end_date))
                except ValueError:
                    pass  
        return tasks, None
