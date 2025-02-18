from ..models.task_category_models import TaskCategory

class TaskCategoryRepository:
    def get_category_by_id(pk):
        try:
            return TaskCategory.objects.get(pk=pk)
        except TaskCategory.DoesNotExist:
            return None

    def get_all_categories():
        return TaskCategory.objects.all()

    def create_category(data):
        category = TaskCategory.objects.create(**data)
        return category

    def update_category(category, data):
        for key, value in data.items():
            setattr(category, key, value)
        category.save()
        return category

    def delete_category(category):
        category.delete()
