from ..components.task_components import TaskComponents
from .base_dispatcher import BaseDispatcher

class TaskDispatcher(BaseDispatcher):
    def get(self, user, model, access_level, data=None, pk=None):
        if access_level == "all":
            return TaskComponents.get_all_tasks()
        elif access_level == "own+below":
            return TaskComponents.get_all_and_below_tasks_assigned_for_user(user)
        elif access_level == "own":
            return TaskComponents.get_all_tasks_assigned_for_user(user)
        return None 
    
    def post(self, user, model, access_level, data, pk=None):
        if access_level == "all":
            return TaskComponents._handle_create_task(user=user, data=data)
        if access_level == "own+below":
            return TaskComponents._handle_create_own_and_below_task(user=user, data=data)
        if access_level == "own":
            return TaskComponents._handle_own_create_task(user=user, data=data)
        return None
    
    def put(self, user, model, access_level, data, pk):
        if access_level == "all":
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == "own+below":
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == "own":
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == "status":
            return TaskComponents.update_task(user, pk, data, access_level)
        return None
        
    def delete(self, user, model, access_level, data, pk):
        if access_level == "all":
            return TaskComponents.delete_task(user, pk)
        return None
