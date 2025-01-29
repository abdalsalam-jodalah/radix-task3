from rest_framework import serializers
from .models import Task

import logging
logger = logging.getLogger("serializers")

class TaskSerializer(serializers.ModelSerializer):
    assigner = serializers.CharField(source='from_user.name', read_only=True)
    assignee = serializers.CharField(source='to_user.name', read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "description",
            "completed",
            "from_user",
            "to_user",
            "assigner",
            "assignee",
        ]

    def validate_name(self, value):
        if not value or len(value.strip()) < 3:
            raise serializers.ValidationError("Task Name must be at least 3 characters long!")
        return value

    def validate_description(self, value):
        if not value.strip():
            raise serializers.ValidationError("Description should not be empty!")
        return value

    def validate_completed(self, value):
        if not isinstance(value, bool):
            raise serializers.ValidationError("Completed must be a boolean value!")
        return value
    
    def create(self, validated_data):
        """Ensure 'from_user' is automatically assigned from the request user."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("User must be authenticated.")

        validated_data["from_user"] = request.user  
        return super().create(validated_data)

    def validate_to_user(self, value):
        """Ensure 'to_user' is not the same as 'from_user'."""
        request = self.context.get("request")
        if request and request.user == value:
            raise serializers.ValidationError("You cannot assign a task to yourself.")
        return value