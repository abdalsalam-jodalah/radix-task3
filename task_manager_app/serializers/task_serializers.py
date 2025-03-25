from rest_framework import serializers
from ..models.task_models import Task
from ..models.user_models import User
import logging
logger = logging.getLogger("serializers")
from ..models.task_category_models import TaskCategory  
from ..models.task_category_models import TaskCategory
from ..constants.task_constants import PriorityChoices, StatusChoices


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    assigner = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        write_only=True,  
        slug_field="email"
    )
    assignee = serializers.SlugRelatedField(
        queryset=User.objects.all(), 
        write_only=True,  
        slug_field="email"
    )
    assigner_detail = UserBriefSerializer(source='assigner', read_only=True)
    assignee_detail = UserBriefSerializer(source='assignee', read_only=True)
    
    category = serializers.SlugRelatedField(
        queryset=TaskCategory.objects.all(), slug_field="name"
    )
    class Meta:
        model = Task
        fields = [
            "id",
            "assigner",
            "assignee",
            "assigner_detail",  
            "assignee_detail",
            'category',
            "name",
            "status",
            "priority",
            "description",
            "start_date",
            "end_date",
            "due_date",
            "created_at",
            "updated_at",
        ]        
        extra_kwargs = {
            "assigner": {"write_only": True},
            "assignee": {"write_only": True, "required": True},
            "name":{"required": True},
            "category": {"required": True},
            "due_date":{"required": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
    def validate_name(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError({"name": "Task name must exist."})
        return value

    def validate_status(self, value):
        if value not in StatusChoices.values:
            raise serializers.ValidationError(
                {"status": f"Invalid status. Choose from {list(StatusChoices.values)}"}
            )
        return value

    def validate_priority(self, value):
        if value not in PriorityChoices.values:
            raise serializers.ValidationError(
                {"priority": f"Invalid priority. Choose from {list(PriorityChoices.values)}"}
            )
        return value
