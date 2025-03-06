from ..models.task_models import Task

class TaskRepository:
    
    def get_task_by_id(pk):
        return Task.objects.filter(pk=pk).first()
    
    def get_all_tasks():
        return Task.objects.all()
    
    def get_tasks_by_user(user):
        return Task.objects.filter(assigner=user.id)
    
    def get_tasks_for_user(user):
        return Task.objects.filter(assignee=user.id)
    
    def create_task(user, validated_data):
        return Task.objects.create( **validated_data)


    def update_task(task, serializer):
        return serializer.save()

    def delete_task(task):
        task.delete()
