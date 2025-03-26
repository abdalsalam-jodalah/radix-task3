import logging
from django.core.exceptions import ValidationError
from ..repositories.task_category_repository import TaskCategoryRepository

logger = logging.getLogger(__name__)

class TaskCategoryComponents:
    @staticmethod
    def get_category(pk):
        try:
            category = TaskCategoryRepository.get_category_by_id(pk)
            if not category:
                raise ValidationError({"error": "Category not found."})
            return category
        except Exception as e:
            logger.error(f"Error in get_category for pk {pk}: {e}")
            raise Exception({"error": f"Error in get_category for pk {pk}: {e}"})

    @staticmethod
    def get_all_categories():
        try:
            categories = TaskCategoryRepository.get_all_categories()
            return categories
        except Exception as e:
            logger.error(f"Error in get_all_categories: {e}")
            raise Exception({"error": f"Error in get_all_categories: {e}"})

    @staticmethod
    def create_category(data):
        try:
            category = TaskCategoryRepository.create_category(data)
            return category
        except Exception as e:
            logger.error(f"Error in create_category: {e}")
            raise Exception({"error": f"Error in create_category: {e}"})

    @staticmethod
    def update_category(pk, data):
        try:
            category = TaskCategoryRepository.get_category_by_id(pk)
            if not category:
                raise ValidationError({"error": "Category not found."})
            updated_category = TaskCategoryRepository.update_category(category, data)
            return updated_category
        except Exception as e:
            logger.error(f"Error in update_category for pk {pk}: {e}")
            raise Exception({"error": f"Error in update_category for pk {pk}: {e}"})

    @staticmethod
    def delete_category(pk):
        try:
            category = TaskCategoryRepository.get_category_by_id(pk)
            if not category:
                raise ValidationError({"error": "Category not found."})
            success = TaskCategoryRepository.delete_category(category)
            return success
        except Exception as e:
            logger.error(f"Error in delete_category for pk {pk}: {e}")
            raise Exception({"error": f"Error in delete_category for pk {pk}: {e}"})
