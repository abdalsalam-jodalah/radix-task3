from rest_framework import serializers
from ..models.task_models import Task
from ..models.user_models import User

import logging
logger = logging.getLogger("serializers")

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Task
        fields = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "description",
            "completed",
            "start_date",
            "end_date",
            "user"
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

        if start_date and end_date and start_date >= end_date:
            raise serializers.ValidationError("Start date must be before the end date.")

        return super().validate(attrs)
