from ..models.task_models import Task
import logging

logger = logging.getLogger("repositories")

class TaskRepository:
    @staticmethod
    def get_task_by_id(pk):
        try:
            task = Task.objects.filter(pk=pk).first()
            return task
        except Exception as e:
            logger.error(f"get_task_by_id failed for pk {pk}: {e}")
            raise Exception({"error": f"get_task_by_id failed for pk {pk}: {e}"})

    @staticmethod
    def get_all_tasks():
        try:
            tasks = list(Task.objects.all())
            return tasks
        except Exception as e:
            logger.error(f"get_all_tasks failed: {e}")
            raise Exception({"error": f"get_all_tasks failed: {e}"})

    @staticmethod
    def get_tasks_by_user(user):
        try:
            tasks = list(Task.objects.filter(assigner=user).order_by('-created_at'))
            return tasks
        except Exception as e:
            logger.error(f"get_tasks_by_user failed for assigner {user.id}: {e}")
            raise Exception({"error": f"get_tasks_by_user failed for assigner {user.id}: {e}"})

    @staticmethod
    def get_tasks_for_user(user):
        try:
            tasks = list(Task.objects.filter(assignee=user).order_by('-created_at'))
            return tasks
        except Exception as e:
            logger.error(f"get_tasks_for_user failed for assignee {user.id}: {e}")
            raise Exception({"error": f"get_tasks_for_user failed for assignee {user.id}: {e}"})

    @staticmethod
    def create_task(user, validated_data):
        try:
            task = Task.objects.create(**validated_data)
            return task
        except Exception as e:
            logger.error(f"create_task failed for user id {user.id}: {e}")
            raise Exception({"error": f"create_task failed for user id {user.id}: {e}"})

    @staticmethod
    def update_task(task, validated_data):
        try:
            for field, value in validated_data.items():
                setattr(task, field, value)
            task.save()
            return task
        except Exception as e:
            logger.error(f"update_task failed for task id {task.id}: {e}")
            raise Exception({"error": f"update_task failed for task id {task.id}: {e}"})

    @staticmethod
    def delete_task(task):
        try:
            task.delete()
            return True
        except Exception as e:
            logger.error(f"delete_task failed for task id {task.id}: {e}")
            raise Exception({"error": f"delete_task failed for task id {task.id}: {e}"})

    @staticmethod
    def get_task_attribute(task, attr):
        try:
            return getattr(task, attr)
        except Exception as e:
            logger.error(f"get_task_attribute failed for task id {task.id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_task_attribute failed for task id {task.id}, attribute {attr}: {e}"})

    @staticmethod
    def set_task_attribute(task, attr, value):
        try:
            setattr(task, attr, value)
            task.save()
            return task
        except Exception as e:
            logger.error(f"set_task_attribute failed for task id {task.id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_task_attribute failed for task id {task.id}, attribute {attr}: {e}"})
