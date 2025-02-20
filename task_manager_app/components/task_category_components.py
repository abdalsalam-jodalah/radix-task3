
from ..repositories.task_category_repository import TaskCategoryRepository

class TaskCategoryComponents:
    def get_category(pk):
        category = TaskCategoryRepository.get_category_by_id(pk)
        if not category:
            return None
        return category

    def get_all_categories():
        categories = TaskCategoryRepository.get_all_categories()
        return categories

    def create_category(data):
        category = TaskCategoryRepository.create_category(data)
        return category

    def update_category(pk, data):
        category = TaskCategoryRepository.get_category_by_id(pk)
        if not category:
            return None
        updated_category = TaskCategoryRepository.update_category(category, data)
        return updated_category

    def delete_category(pk):
        category = TaskCategoryRepository.get_category_by_id(pk)
        if not category:
            return None
        TaskCategoryRepository.delete_category(category)
        return True
