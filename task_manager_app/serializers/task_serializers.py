from rest_framework import serializers
from ..models.task_models import Task
from ..models.user_models import User
import logging
logger = logging.getLogger("serializers")

class TaskSerializer(serializers.ModelSerializer):
    assigner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Assigner (who assigns the task)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Assignee (who receives the task)

    class Meta:
        model = Task
        fields = [
            "id",
            "created_at",
            "updated_at",
            "assigner",
            "assignee",
            "name",
            "status",
            "priority",
            "description",
            "start_date",
            "end_date",
        ]

    def validate_name(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Task name must be at least 3 characters long.")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description cannot be empty.")
        return value

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        assigner = attrs.get("assigner")
        assignee = attrs.get("assignee")

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Start date must be before the end date.")

        # if assigner == assignee:
        #     raise serializers.ValidationError("Assigner and assignee cannot be the same person.")

        return super().validate(attrs)

    def validate_status(self, value):
        if value not in Task.StatusChoices.values:
            raise serializers.ValidationError(f"Invalid status. Choose from {Task.StatusChoices.choices}")
        return value
            
    def validate_priority(self, value):
        if value not in Task.PriorityChoices.values:
            raise serializers.ValidationError(f"Invalid priority. Choose from {Task.PriorityChoices.choices}")
        return value
