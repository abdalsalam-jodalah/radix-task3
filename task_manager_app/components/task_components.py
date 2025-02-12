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
