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
from datetime import datetime
from django.utils import timezone
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
    def get_all_tasks_assigned_by_user(user):
        try:
            tasks = TaskRepository.get_tasks_by_user(user)
            if not tasks:
                return []
            return tasks 
        except Exception as e:
            logger.error(f"Error in get_tasks_assigned_by_user: {e}")
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
            filtered_tasks = tasks

            if search_query:
                query_lower = search_query.lower()
                filtered_tasks = [
                    task for task in filtered_tasks 
                    if (hasattr(task, 'name') and query_lower in task.name.lower()) or
                    (hasattr(task, 'description') and query_lower in task.description.lower())
                ]
        
            if filters:
                if 'priority' in filters and filters['priority']:
                    filtered_tasks = [
                        task for task in filtered_tasks 
                        if getattr(task, 'priority', None) == filters['priority']
                    ]
                if 'status' in filters and filters['status']:
                    filtered_tasks = [
                        task for task in filtered_tasks 
                        if getattr(task, 'status', None) == filters['status']
                    ]
                if 'category' in filters and filters['category']:
                    filtered_tasks = [
                        task for task in filtered_tasks 
                        if getattr(task, 'category', None).name == filters['category']
                    ]               
                if ('start_date' in filters and 'end_date' in filters and 'due_date' in filters and
                        filters['start_date'] and filters['end_date']):
                    try:
                        start_date_naive = datetime.strptime(filters['start_date'], "%Y-%m-%d %H:%M:%S")
                        end_date_naive = datetime.strptime(filters['end_date'], "%Y-%m-%d %H:%M:%S")
                        start_date = timezone.make_aware(start_date_naive)
                        end_date = timezone.make_aware(end_date_naive)
                        
                        filtered_tasks = [
                            task for task in filtered_tasks 
                            #TODO: back here
                            if start_date <= task.start_date <= end_date and start_date <= task.end_date <= end_date
                        ]
                    except ValueError as err:
                        #skip this filter
                        pass
                if ('due_date' in filters and filters['due_date']):
                    try:
                        due_date_naive = datetime.strptime(filters['due_date'], "%Y-%m-%d %H:%M:%S")
                        due_date = timezone.make_aware(due_date_naive)
                        
                        filtered_tasks = [
                            task for task in filtered_tasks 
                            if task.due_date <= due_date
                        ]
                    except ValueError as err:
                        #skip this filter
                        pass

            return filtered_tasks   
        except Exception as e:
            logger.error(f"Error in get_task_from_tasks: {e}")
            raise e
        
    @staticmethod    
    def fetch_task_data_from_req(request, user, method):
        try:
            body_data = json.loads(request.body.decode('utf-8')) 
        except json.JSONDecodeError:
            body_data = {}  
        if not body_data:
            raise ValidationError ({"error":"missing body data, try again"}) 
        keys = ["name", "description", "status", "priority", "start_date", "end_date", "assigner", "assignee", "category", "due_date"]
        data = {key: body_data[key] for key in keys if key in body_data}
        
        if method == "post" and not data.get("assigner"):
            data["assigner"] = user.email
        
        partial = False
        if method == "patch":
            partial = True
        serializer = TaskSerializer(data=data, partial=partial)
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

    
    
    @staticmethod
    def handle_update_any_task(user, id, task_data):
        try:
        
            old_task = TaskRepository.get_task_by_id(id)
            task = TaskRepository.update_task(old_task, task_data)
            return task
        except Exception as e:
            logger.error(f"Error in updating: {e}")
            raise e

    @staticmethod
    def handle_update_own_below_task (user, id, task_data):
        try:       
            old_task = TaskRepository.get_task_by_id(id)

            if old_task.assignee.id != user.id: # check own part
                if not old_task.assignee.parent:# check below part
                    raise ValidationError({"error": "Permission denied, u cant update this task, nobody can assign him a task except himself!"})
                if user != old_task.assignee.parent: 
                    if not old_task.assignee.parent.parent:
                        raise ValidationError({"error": "Permission denied, u cant update this task, only his parent can update his task!"})
                    if user != old_task.assignee.parent.parent:
                        raise ValidationError({"error": "Permission denied, u cant update this task"})
                    
            task = TaskRepository.update_task(old_task, task_data)
            if task and isinstance(task, Task):
               return task
            raise  ValidationError({"error": "error while updating data"})
        except Exception as e:
            logger.error(f"Error in updating: {e}")
            raise e

    @staticmethod
    def handle_update_own_task(user, id, task_data):
        try:
            old_task = TaskRepository.get_task_by_id(id)
            if old_task.assignee.id != user.id:
                raise ValidationError({"error": "You can only update your own tasks"})     
            task = TaskRepository.update_task(old_task, task_data)
            if task and isinstance(task, Task):
               return task
            raise  ValidationError({"error": "error while updating data"})
        except Exception as e:
            logger.error(f"Error in updating: {e}")
            raise e
        
    @staticmethod
    def delete_task(user, pk):
        try:
            task = TaskRepository.get_task_by_id(pk)
            TaskRepository.delete_task(task)
            return {"detail": "Task deleted successfully"}
        except Exception as e:
            logger.error(f"Error in updating: {e}")
            raise e
        