from rest_framework.response import Response
from ..components.task_components import TaskComponents as TC
from ..components.user_components import UserComponents as UC
from ..models.task_models import Task, User

class TaskComponents():
    def get_log_message( action, user, task_id=None, additional_info=""):
        """
        Formatter function to create dynamic log messages.
        """
        message = f"[TaskApi][{action}] User {user.id} - {additional_info}"
        if task_id:
            message += f" - Task {task_id}"
        return message
    
