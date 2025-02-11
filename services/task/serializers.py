from rest_framework import serializers
from .models import Task
from datetime import datetime
from services.user.models import User

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
    
    def validate(self, attrs):
        for field in ["start_date", "end_date"]:
            if not isinstance(attrs.get(field), datetime):
                raise serializers.ValidationError({field: "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SSZ'."})

        return super().validate(attrs)
    