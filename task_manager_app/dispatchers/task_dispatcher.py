from ..components.task_components import TaskComponents
from .base_dispatcher import BaseDispatcher
from ..constants.access_levels import AccessLevel
from ..serializers.task_serializers import TaskSerializer
from django.core.exceptions import ValidationError
from rest_framework.exceptions import NotAcceptable

class TaskDispatcher(BaseDispatcher):
    def get(self, user, model, access_level, data=None, pk=None):
        if access_level == AccessLevel.ALL.value:
            return TaskComponents.get_all_tasks()
        elif access_level == AccessLevel.OWN_BELOW.value:
            return TaskComponents.get_all_and_below_tasks_assigned_for_user(user)
        elif access_level == AccessLevel.OWN.value:
            return TaskComponents.get_all_tasks_assigned_for_user(user)
        raise ValidationError({"error": "Invalid access level"})
    
    def post(self, user, model, access_level, data, pk=None):
        if access_level==AccessLevel.ALL.value:
            return TaskComponents.handle_create_task_for_all(user, data)
        if access_level == AccessLevel.OWN_BELOW.value:
            return TaskComponents.handle_create_own_and_below_task(user, data)
        if access_level == AccessLevel.OWN.value:
            return TaskComponents.handle_create_own_task( user, data)
        raise ValidationError({"error": "Invalid access level"})
    
    def put(self, user, model, access_level, data, pk):
        if access_level == AccessLevel.ALL.value:
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == AccessLevel.OWN_BELOW.value:
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == AccessLevel.OWN.value:
            return TaskComponents.update_task(user, pk, data, access_level)
        elif access_level == "status":
            return TaskComponents.update_task(user, pk, data, access_level)
        raise ValidationError({"error": "Invalid access level"})
        
    def delete(self, user, model, access_level, data, pk):
        if access_level == AccessLevel.ALL.value:
            return TaskComponents.delete_task(user, pk)
        elif access_level == AccessLevel.OWN_BELOW.value or access_level == AccessLevel.OWN.value:
            raise NotAcceptable({"error": "You don't have permissions"})
        raise ValidationError({"error": "Invalid access level"})
