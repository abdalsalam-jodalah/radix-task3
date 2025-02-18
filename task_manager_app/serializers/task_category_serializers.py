from rest_framework import serializers
from ..models.task_category_models import TaskCategory

class TaskCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCategory
        fields = ['id', 'name', 'description']