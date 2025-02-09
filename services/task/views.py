from rest_framework import generics, permissions  
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .models import Task

import logging
auth_logger = logging.getLogger("auth")
logger = logging.getLogger("views")

# class IsAdminOrOwner(BasePermission):
#     """ Allow admin to do anything, but users can only manage their own tasks """
#     def has_permission(self, request, view):
#         return request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         if request.user.role == "admin":
#             return True
#         return obj.to_user == request.user

class TaskListView(generics.ListAPIView):
    """ Admin sees all tasks, user sees only their tasks """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        return Task.objects.filter(to_user=user)

class TaskDetailView(generics.RetrieveAPIView):
    """ Admin sees all tasks, user sees only their tasks """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  
    queryset = Task.objects.all()
 
    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        return Task.objects.filter(to_user=user)


class TaskCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                task = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Validation error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class TaskUpdateView(generics.UpdateAPIView):
    """ Admin can update any task, user can update only their assigned tasks """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  
    queryset = Task.objects.all()
