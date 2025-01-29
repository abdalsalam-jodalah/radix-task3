from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .models import Task
from .serializers import TaskSerializer

import logging
auth_logger = logging.getLogger("auth")
logger = logging.getLogger("views")

class IsAdminOrOwner(BasePermission):
    """ Allow admin to do anything, but users can only manage their own tasks """
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == "admin":
            return True
        return obj.to_user == request.user

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
    permission_classes = [IsAdminOrOwner]
    queryset = Task.objects.all()
 
    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        return Task.objects.filter(to_user=user)

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def perform_create(self, serializer):
        if self.from_user is None:
            serializer.save(from_user=self.request.user)


class TaskUpdateView(generics.UpdateAPIView):
    """ Admin can update any task, user can update only their assigned tasks """
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrOwner]
    queryset = Task.objects.all()
