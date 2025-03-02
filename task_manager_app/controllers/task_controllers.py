
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..permissions.role_based_permissions import HasRolePermission  
from ..pagination import CustomPagination
from ..components.auth_comopnents import AuthComponents as AC
from ..components.task_components import TaskComponents
from ..serializers.task_serializers import TaskSerializer
from ..models.email_notification_model import EmailNotification
from ..components.task_notification import send_task_notification
from ..models.user_models import User
from ..models.task_models import Task
import logging 
from ..components.role_permission_components import RolePermissionComponent
import traceback

logger = logging.getLogger("views")

class TaskApi(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice, HasRolePermission]
    pagination_class = CustomPagination
   
    def get(self, request, pk=None):
        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
            filtered_perms = RolePermissionComponent.get_action_permissions(perms, action="get")
            if filtered_perms: 
                for perm in filtered_perms:
                    model, action, access_level = perm["model"], perm["action"], perm["access_level"]
                    result = RolePermissionComponent.dispatch(user, model, action, access_level)
            else:
                print("No matching permissions found.")
                result = None 

            if result is None:
                return Response({"error": "You dont have permissions "}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            if pk:
                task, response_data = TaskComponents.get_task_from_tasks(result, pk)
                if task is None or isinstance(task, Task ):
                    return Response(response_data, status=response_status)
                return Response(response_data, status=response_status)
            
            filters = {
                "priority": request.GET.get("priority"),
                "status": request.GET.get("status"),
                "category": request.GET.get("category"),
                "start_date": request.GET.get("start_date"),
                "end_date": request.GET.get("end_date"),
            }
             
            tasks, response_status = TaskComponents.get_tasks_filtered(result, filters)
            if tasks is None:
                return Response(response_status, status=status.HTTP_404_NOT_FOUND)
            paginator = self.pagination_class()
            paginated_tasks = paginator.paginate_queryset(tasks, request)
            
            if paginated_tasks is None:
                return Response({"error": "No tasks available for the given filters."}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(paginated_tasks, many=True)
            return paginator.get_paginated_response(serializer.data)

        except Exception as e:
            logger.error(f"Error getting task: {e.with_traceback( e.__traceback__)}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try: 
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = TaskComponents.fetch_user_data(request)

            perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
            filtered_perms = RolePermissionComponent.get_action_permissions(perms, action="post")
            if filtered_perms: 
                for perm in filtered_perms:
                    model, action, access_level = perm["model"], perm["action"], perm["access_level"]
                    result = RolePermissionComponent.dispatch(user, model, action, access_level, data)
            else:
                print("No matching permissions found.")
                result = None 

            if result is None:
                return Response({"error": "You dont have permissions "}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            task, response_status = result

            if task and task.name:
                notification = EmailNotification.objects.create(
                    user=user,
                    message=f"You have been assigned a new task: {task.name}",
                    task=task
                )
                send_task_notification.delay(notification.id)
                return Response( {"task": TaskSerializer(task).data}, status.HTTP_201_CREATED )
            
            status_code = response_status.get("status")
            return Response(
                {"task": TaskSerializer(task).data} if task else {"error": "Invalid request"},
                status=int(status_code)
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}\n{traceback.format_exc()}")
            return Response({"error": f"Invalid request: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk=None):

        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
            filtered_perms = RolePermissionComponent.get_action_permissions(perms, action="put")
            if filtered_perms: 
                for perm in filtered_perms:
                    model, action, access_level = perm["model"], perm["action"], perm["access_level"]
                    result = RolePermissionComponent.dispatch(user, model, action, access_level, request.data, pk)
            else:
                print("No matching permissions found.")
                result = None 

            if result is None:
                return Response({"error": "You dont have permissions "}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            response_data, response_status = result
            return Response(response_data, status=response_status)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            perms = RolePermissionComponent.get_permissions_by_role_decoded(user.role)
            filtered_perms = RolePermissionComponent.get_action_permissions(perms, action="delete")
            if filtered_perms: 
                for perm in filtered_perms:
                    model, action, access_level = perm["model"], perm["action"], perm["access_level"]
                    result = RolePermissionComponent.dispatch(user, model, action, access_level)
            else:
                print("No matching permissions found.")
                result = None 

            if result is None:
                return Response({"error": "You dont have permissions "}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
            response_data, response_status = result
            return Response(response_data, status=response_status)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, pk=None):
        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            response_data, response_status = TaskComponents.partial_update_task(user, pk,request.data)
            return Response(response_data, status=response_status)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

class ByUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request,pk=None):
        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            if pk:
                task, response_data, response_status = TaskComponents.get_task_response(user, pk)

                if task is None or isinstance(task, Task ):
                    return Response(response_data, status=response_status)
                return Response(response_data, status=response_status)
            
            filters = {
                "priority": request.GET.get("priority"),
                "status": request.GET.get("status"),
                "category": request.GET.get("category"),
                "start_date": request.GET.get("start_date"),
                "end_date": request.GET.get("end_date"),
            }
            search_query = request.GET.get("search", None)
            tasks = TaskComponents.get_tasks_assigned_by_user(user, filters)
            
            paginator = self.pagination_class()
            paginated_tasks = paginator.paginate_queryset(tasks, request)

            if paginated_tasks is None:
                return Response({"error": "No tasks available for the given filters."}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(paginated_tasks, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:  
            logger.error(f"Error getting task: {e}")
            return Response({"error": f"Invalid request:  {e} \n{e.with_traceback(e.__traceback__)}"}, status=status.HTTP_400_BAD_REQUEST)
   