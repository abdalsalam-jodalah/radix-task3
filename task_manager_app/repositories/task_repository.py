from ..models.task_models import Task

class TaskRepository:
    
    def get_task_by_id(pk):
        return Task.objects.filter(pk=pk).first()
    
    def get_all_tasks():
        return Task.objects.all()
    
    def get_tasks_by_user(user):
        return Task.objects.filter(user=user)
    
    def create_task(user, serializer):
        return serializer.save(user=user)

    def update_task(task, serializer):
        return serializer.save()

    def delete_task(task):
        task.delete()
