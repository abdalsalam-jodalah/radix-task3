from ..models.task_category_models import TaskCategory
import logging

logger = logging.getLogger("repositories")

class TaskCategoryRepository:
    @staticmethod
    def get_category_by_id(pk):
        try:
            category = TaskCategory.objects.get(pk=pk)
            return category
        except TaskCategory.DoesNotExist:
            logger.info(f"get_category_by_id: Category with pk {pk} not found")
            return None
        except Exception as e:
            logger.error(f"get_category_by_id failed for pk {pk}: {e}")
            raise Exception({"error": f"get_category_by_id failed for pk {pk}: {e}"})

    @staticmethod
    def get_all_categories():
        try:
            categories = list(TaskCategory.objects.all())
            return categories
        except Exception as e:
            logger.error(f"get_all_categories failed: {e}")
            raise Exception({"error": f"get_all_categories failed: {e}"})

    @staticmethod
    def create_category(data):
        try:
            category = TaskCategory.objects.create(**data)
            return category
        except Exception as e:
            logger.error(f"create_category failed: {e}")
            raise Exception({"error": f"create_category failed: {e}"})

    @staticmethod
    def update_category(category, data):
        try:
            for key, value in data.items():
                setattr(category, key, value)
            category.save()
            return category
        except Exception as e:
            cat_id = getattr(category, 'id', 'N/A')
            logger.error(f"update_category failed for category id {cat_id}: {e}")
            raise Exception({"error": f"update_category failed for category id {cat_id}: {e}"})

    @staticmethod
    def delete_category(category):
        try:
            category.delete()
            return True
        except Exception as e:
            cat_id = getattr(category, 'id', 'N/A')
            logger.error(f"delete_category failed for category id {cat_id}: {e}")
            raise Exception({"error": f"delete_category failed for category id {cat_id}: {e}"})

    @staticmethod
    def get_category_attribute(category, attr):
        try:
            return getattr(category, attr)
        except Exception as e:
            cat_id = getattr(category, 'id', 'N/A')
            logger.error(f"get_category_attribute failed for category id {cat_id}, attribute {attr}: {e}")
            raise Exception({"error": f"get_category_attribute failed for category id {cat_id}, attribute {attr}: {e}"})

    @staticmethod
    def set_category_attribute(category, attr, value):
        try:
            setattr(category, attr, value)
            category.save()
            return category
        except Exception as e:
            cat_id = getattr(category, 'id', 'N/A')
            logger.error(f"set_category_attribute failed for category id {cat_id}, attribute {attr}: {e}")
            raise Exception({"error": f"set_category_attribute failed for category id {cat_id}, attribute {attr}: {e}"})
