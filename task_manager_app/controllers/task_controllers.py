
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
import traceback
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from ..permissions.user_permissions import IsSingleDeviceANDIsAuthenticatedAndUpdateStatus
from ..pagination import CustomPagination
from ..components.auth_components import AuthComponents 
from ..components.task_components import TaskComponents
from ..serializers.task_serializers import TaskSerializer
from ..models.email_notification_models import EmailNotification
from ..components.task_notification import send_task_notification
from ..models.user_models import User
from ..models.task_models import Task
from ..components.role_permission_components import RolePermissionComponent
from ..decorators.handle_exceptions import handle_exceptions

import logging 
logger = logging.getLogger("controllers")

class TaskApi(APIView):
    authentication_classes = []

    pagination_class = CustomPagination
    permission_classes = [IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]
    
    @handle_exceptions
    def get(self, request, id=None):
        user = AuthComponents.fetch_user_from_req(request)
        tasks = RolePermissionComponent.handle_action(user, "task", "get")
        if not tasks:
                return Response(tasks, status=status.HTTP_200_OK)
        if id:
            task = TaskComponents.get_task_from_tasks(tasks, id)
            return Response(TaskSerializer(task).data,  status=status.HTTP_200_OK)
        
        search_query = request.GET.get("search", None)
        filters = {
            "priority": request.GET.get("priority"),
            "status": request.GET.get("status"),
            "category": request.GET.get("category"),
            "start_date": request.GET.get("start_date"),
            "end_date": request.GET.get("end_date"),
            "due_date": request.GET.get("due_date"),
        }
        filtered_tasks = TaskComponents.get_tasks_filtered(tasks, filters, search_query)
        
        paginator = self.pagination_class()
        paginated_tasks = paginator.paginate_queryset(filtered_tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)
    


    @handle_exceptions
    def post(self, request):    
        user = AuthComponents.fetch_user_from_req(request)
        data = TaskComponents.fetch_task_data_from_req(request, user, "post")
        task = RolePermissionComponent.handle_action(user, "task", "post", data=data)
        
        notification = EmailNotification.objects.create(
            user=user,
            message=f"You have been assigned a new task: {task.name}",
            task=task
        )
        send_task_notification.delay(notification.id)
        return Response( {"task": TaskSerializer(task).data}, status.HTTP_201_CREATED )



    @handle_exceptions
    def put(self, request, id=None):
        if id == None:
            return Response({"error": "Missing task id, or not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AuthComponents.fetch_user_from_req(request)
        data = TaskComponents.fetch_task_data_from_req(request, user, "put")
        task = RolePermissionComponent.handle_action(user=user, action_model="task",action= "put",data=data, pk=id)
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
    


    @handle_exceptions
    def patch(self, request, id=None):
        if id == None:
            return Response({"error": "Missing task id, or not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AuthComponents.fetch_user_from_req(request)
        data = TaskComponents.fetch_task_data_from_req(request, user, "patch")
        task = RolePermissionComponent.handle_action(user=user, action_model="task",action= "put",data=data, pk=id)
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)
    
       
    @handle_exceptions 
    def delete(self, request, id=None):
        if id == None:
            return Response({"error": "Missing task id, or not found."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = AuthComponents.fetch_user_from_req(request)
        message = RolePermissionComponent.handle_action(user, "task", "delete", id=id)
        return Response(message, status=status.HTTP_200_OK)
    


class TaskApiByUser(APIView):
    pagination_class = CustomPagination
    authentication_classes = []
    permission_classes = [IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]

    @handle_exceptions
    def get(self, request,id=None):
        user = AuthComponents.fetch_user_from_req(request)
        tasks = TaskComponents.get_all_tasks_assigned_by_user(user)
        if not tasks:
                return Response(tasks, status=status.HTTP_200_OK)
        if id:
            task = TaskComponents.get_task_from_tasks(tasks, id)
            return Response(TaskSerializer(task).data,  status=status.HTTP_200_OK)
        
        search_query = request.GET.get("search", None)
        filters = {
            "priority": request.GET.get("priority"),
            "status": request.GET.get("status"),
            "category": request.GET.get("category"),
            "start_date": request.GET.get("start_date"),
            "end_date": request.GET.get("end_date"),
            "due_date": request.GET.get("due_date"),
        }
        filtered_tasks = TaskComponents.get_tasks_filtered(tasks, filters, search_query)
        
        paginator = self.pagination_class()
        paginated_tasks = paginator.paginate_queryset(filtered_tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)
        