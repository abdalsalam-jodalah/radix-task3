from datetime import datetime
from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from rest_framework import status
from rest_framework.response import Response
import json

from ..serializers.task_serializers import TaskSerializer
from ..repositories.task_repository import TaskRepository
from ..components.shared_components import SharedComponents as SC
from ..models.task_models import Task
import logging
from django.core.exceptions import ValidationError

logger = logging.getLogger("components")

class TaskComponents:
    @staticmethod
    def get_all_tasks():
        try:
            tasks = TaskRepository.get_all_tasks()
            if not tasks:
                return []
            return tasks
        except Exception as e:
            logger.error(f"Error in get_all_tasks: {e}")
            raise e
        
    @staticmethod       
    def get_all_and_below_tasks_assigned_for_user(user):
        try:
            assigned_tasks = TaskRepository.get_tasks_for_user(user)  
            assigned_by_user_tasks = TaskRepository.get_tasks_by_user(user) 
            all_tasks = list(assigned_tasks) + list(assigned_by_user_tasks)
            if not all_tasks:
                return []
            return all_tasks 
        except Exception as e:
            logger.error(f"Error in get_all_and_below_tasks_assigned_for_user: {e}")
            raise e
        
    @staticmethod
    def get_all_tasks_assigned_for_user (user, filters=None, search_query=None):
        try:
            tasks = TaskRepository.get_tasks_for_user(user)
            if not tasks:
                return []
            return tasks 
        except Exception as e:
            logger.error(f"Error in get_all_tasks_assigned_for_user: {e}")
            raise e
        
    @staticmethod
    def get_task_from_tasks(tasks, pk):
        try:
            for task in tasks:
                if isinstance(task, Task) and task.id == pk:
                    return task
                if isinstance(task, dict) and task.get("id") == pk:
                    return task
                elif hasattr(task, "id") and task.id == pk:
                    return task
            raise ValidationError({"error": "Task not found!"})
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e
        
    @staticmethod    
    def get_tasks_filtered(tasks, filters=None, search_query=None):
        try:
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
               
                #TODO: due_date 
                if ('start_date' in filters and 'end_date' in filters and
                filters['start_date'] and filters['end_date']):
                    try:
                        start_date = datetime.strptime(filters['start_date'], "%Y-%m-%d")
                        end_date = datetime.strptime(filters['end_date'], "%Y-%m-%d")
                        tasks = tasks.filter(due_date__range=(start_date, end_date))
                    except ValueError:
                        pass

            return tasks   
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e
        
    @staticmethod    
    def fetch_task_data_from_req(request, user):
        try:
            body_data = json.loads(request.body.decode('utf-8')) 
        except json.JSONDecodeError:
            body_data = {}  
        if not body_data:
            raise ValidationError ({"error":"missing body data, try again"}) 
        
        data= {
            "name": body_data.get("name"),
            "description": body_data.get("description"),
            "status": body_data.get("status"),
            "priority": body_data.get("priority"),
            "start_date": body_data.get("start_date"),
            "end_date": body_data.get("end_date"),
            "assigner": body_data.get("assigner"),
            "assignee": body_data.get("assignee"),
            "category": body_data.get("category"),
            "due_date": body_data.get("due_date")
        }
        if not data["assigner"]:
             data["assigner"]= user.email
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            return serializer.validated_data
        raise ValidationError ({"error":f"data incorrect {serializer.errors}"})  
    


    @staticmethod
    def handle_create_task_for_all(user, task_data):
        try: 
            task = TaskRepository.create_task(user, task_data)

            if task and isinstance(task, Task):
                return task
            raise ValidationError({"error":"error in creating task, try again "})
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e
        
    @staticmethod
    def handle_create_own_and_below_task(user, task_data):
        try:
            if task_data["assignee"].id != user.id: # check own part
                if not task_data["assignee"].parent:# check below part
                    raise ValidationError({"error": "Permission denied, u cant assign this user any task, nobody can assign him a task!"})
                if user != task_data["assignee"].parent: 
                    if not task_data["assignee"].parent.parent:
                        raise ValidationError({"error": "Permission denied, u cant assign this user any task, only his parent can assign him a task!"})
                    if user != task_data["assignee"].parent.parent:
                        raise ValidationError({"error": "Permission denied, u cant assign this user any task"})
                
            task = TaskRepository.create_task(user, task_data)
            if task and isinstance(task, Task):
                return task      
            raise ValidationError({"error":"error in creating task, try again "})
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e
 
    @staticmethod
    def handle_create_own_task(user, task_data):
        try:
            if task_data["assignee"].id != user.id: 
                raise ValidationError({"error": "You can only assign tasks to yourself"})
            task = TaskRepository.create_task(user, task_data)
            if task and isinstance(task, Task):
                return task
            raise ValidationError({"error":"error in creating task, try again "})
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e      

    # @staticmethod
    # def is_parent_of_child(parent, child)
    def get_task_response(user, pk):
        task = TaskRepository.get_task_by_id(pk)
        if not task and not isinstance(task, Task):
            return None, {"detail": "Task not found"}, 404
        serializer = TaskSerializer(task)
       
        
        if user.role != "admin" and serializer.data.get('assignee') != user.id:
            raise PermissionDenied("You can only view your own tasks.")
        return task, serializer.data, 200
        

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
    



    
 

