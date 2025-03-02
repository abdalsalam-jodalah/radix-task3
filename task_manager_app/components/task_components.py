from datetime import datetime
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework import status
from rest_framework.response import Response
from ..serializers.task_serializers import TaskSerializer
from ..repositories.task_repository import TaskRepository
from ..components.shared_components import SharedComponents as SC
from ..models.task_models import Task
import json
class TaskComponents:
    def get_task_response(user, pk):
        task = TaskRepository.get_task_by_id(pk)
        if not task and not isinstance(task, Task):
            return None, {"detail": "Task not found"}, 404
        serializer = TaskSerializer(task)
       
        
        if user.role != "admin" and serializer.data.get('assignee') != user.id:
            raise PermissionDenied("You can only view your own tasks.")
        return task, serializer.data, 200
    def get_task_from_tasks(tasks, pk):
        for task in tasks:
            if isinstance(task, dict) and task.get("id") == pk:
                return task, {"message": "Task found", "task": task}
            elif hasattr(task, "id") and task.id == pk:
                return task, {"message": "Task found", "task": task}

        return None, {"message": "Task not found", "task": None}

    def create_task(user, data):
        serializer = TaskSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            task = TaskRepository.create_task(user, serializer)
            return serializer.data, 201
        return None, {"detail": "Invalid data"}, 400

    def update_task(user, pk, data, access_level):
        
        task = TaskRepository.get_task_by_id(pk)
        if not task:
            return None, {"detail": "Task not found"}, 404

        if access_level == "own" and task.assignee_id != user.id:
            return None, {"detail": "You can only update your own tasks"}, 403

        if access_level == "own+below":
            if task.assignee_id != user.id and not TaskRepository.is_user_below(user, task.assignee_id):
                return None, {"detail": "You can only update your tasks or those of your subordinates"}, 403

        if access_level == "status":
            allowed_fields = ["status"]
            if any(field not in allowed_fields for field in data.keys()):
                return None, {"detail": "You can only update the status field"}, 403

        serializer = TaskSerializer(task, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            TaskRepository.update_task(task, serializer)
            return serializer.data, 200

        return None, {"detail": "Invalid data"}, 400

    def delete_task(user, pk):
        task = TaskRepository.get_task_by_id(pk)
        if not task:
            return {"detail": "Task not found"}, 404
        if user.role != "admin" and task.assignee != user:
            raise PermissionDenied("You can only delete your own tasks.")

        TaskRepository.delete_task(task)
        return {"detail": "Task deleted successfully"}, 204
    
    def partial_update_task(user, pk, data):
        pass
    def get_all_tasks():
        return TaskRepository.get_all_tasks()
        
    def get_tasks_assigned_by_user(user, filters=None, search_query=None):
        tasks = TaskRepository.get_tasks_by_user(user).order_by('-created_at')
        if not tasks:
            return {"detail": "Tasks not found for this user"}, 404
        filterd_tasks, error = TaskComponents.get_tasks_filtered(tasks, filters, search_query)
        return filterd_tasks
    
    def get_tasks_assigned_for_user (user, filters=None, search_query=None):
        tasks = TaskRepository.get_tasks_for_user(user).order_by('-created_at')
        if not tasks:
            return None, {"detail": "Tasks not found fro this user"}
        filterd_tasks, error = TaskComponents.get_tasks_filtered(tasks, filters, search_query)
        return filterd_tasks
    
    def get_all_tasks_assigned_for_user (user, filters=None, search_query=None):
        tasks = TaskRepository.get_tasks_for_user(user).order_by('-created_at')
        if not tasks:
            return None, {"detail": "Tasks not found fro this user"}
        return tasks
    def get_all_and_below_tasks_assigned_for_user(user):

        assigned_tasks = TaskRepository.get_tasks_for_user(user)  
        assigned_by_user_tasks = TaskRepository.get_tasks_by_user(user) 
        all_tasks = list(assigned_tasks.order_by('-created_at')) + list(assigned_by_user_tasks.order_by('-created_at'))

        return all_tasks if all_tasks else None

    def get_tasks_filtered(tasks, filters=None, search_query=None):
        if search_query:
            tasks = tasks.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        if filters:
            if 'priority' in filters and filters['priority']:
                tasks = tasks.filter(priority=filters['priority'])
            
            if 'status' in filters and filters['status']:
                tasks = tasks.filter(status=filters['status'])

            if 'category' in filters and filters['category']:
                tasks = tasks.filter(category=filters['category'] )

            # if 'start_date' in filters and 'end_date' in filters and filters['start_date'] and filters['end_date']:
            #     try:
            #         start_date = datetime.strptime(filters['start_date'], "%Y-%m-%d")
            #         end_date = datetime.strptime(filters['end_date'], "%Y-%m-%d")
            #         tasks = tasks.filter(created_at__range=(start_date, end_date))
            #     except ValueError:
            #         pass  

        return tasks, None
    
    def _handle_create_task( user, data):
        
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = TaskRepository.create_task(user, serializer.validated_data)
            return task, status.HTTP_201_CREATED
        
        return None, Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def _handle_create_own_and_below_task(user, data):
     
        if "assignee" in data and data["assignee"] != user.id:
            if not TaskRepository.is_user_below(user, data["assignee"]):
                return None, Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = TaskRepository.create_task(user, serializer.validated_data)
            return task, status.HTTP_201_CREATED
        return None, Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
    
    def _handle_own_create_task(user, data):
    
        if "assignee" in data and data["assignee"] != user.id:
            return None, Response({"detail": "You can only assign tasks to yourself"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = TaskRepository.create_task(user, serializer.validated_data)
            return task, status.HTTP_201_CREATED
        return None
              
    def fetch_user_data(request):
        try:
            body_data = json.loads(request.body.decode('utf-8')) 
        except json.JSONDecodeError:
            body_data = {}  
        
        return {
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "status": body_data.get("status"),
            "priority": body_data.get("priority"),
            "start_date": body_data.get("start_date"),
            "end_date": body_data.get("end_date"),
            "assigner": body_data.get("assigner"),
            "assignee": body_data.get("assignee"),
            "category": body_data.get("category")
        }
