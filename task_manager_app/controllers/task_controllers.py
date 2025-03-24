
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable
import traceback
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed

from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..permissions.role_based_permissions import HasRolePermission  
from ..pagination import CustomPagination
from ..components.auth_components import AuthComponents 
from ..components.task_components import TaskComponents
from ..serializers.task_serializers import TaskSerializer
from ..models.email_notification_models import EmailNotification
from ..components.task_notification import send_task_notification
from ..models.user_models import User
from ..models.task_models import Task
from ..components.role_permission_components import RolePermissionComponent

import logging 
logger = logging.getLogger("controllers")

class TaskApi(APIView):
    authentication_classes = []
    # permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice, HasRolePermission]
    # permission_classes = [ IsSingleDevice ]
    pagination_class = CustomPagination
   
    def get(self, request, id=None):
        try:
            user = AuthComponents.fetch_user_from_req(request)
            tasks = RolePermissionComponent.handle_action(user, "task", "get")
            if not tasks:
                 return Response(tasks, status=status.HTTP_200_OK)
            if id:
                task = TaskComponents.get_task_from_tasks(tasks, id)
                return Response(task,  status=status.HTTP_200_OK)
            
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
        
        except ValueError as err:
             return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except NotAcceptable as err:
            return Response({"error": str(err)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try: 
            user = AuthComponents.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = TaskComponents.fetch_user_data(request)

            result = RolePermissionComponent.handle_action(user, "task", "post",data=data)

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
        except NotAcceptable as exp:
                return Response({"error": f"{exp}"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            logger.error(f"Error creating task: {e}\n{traceback.format_exc()}")
            return Response({"error": f"Invalid request: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, id=None):

        try:
            user = AuthComponents.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            result = RolePermissionComponent.handle_action(user, "task", "put",data=request.data, id=id)
           
            response_data, response_status = result
            return Response(response_data, status=response_status)
        except NotAcceptable as exp:
                return Response({"error": f"{exp}"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, id=None):
        try:
            user = AuthComponents.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            result = RolePermissionComponent.handle_action(user,  "task","delete",id=id)

            response_data, response_status = result
            return Response(response_data, status=response_status)
        except NotAcceptable as exp:
                return Response({"error": f"{exp}"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request, id=None):
        try:
            user = AuthComponents.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
            response_data, response_status = TaskComponents.partial_update_task(user, id,request.data)
            return Response(response_data, status=response_status)
        except NotAcceptable as exp:
                return Response({"error": f"{exp}"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

class ByUser(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request,id=None):
        try:
            user = AuthComponents.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            if id:
                task, response_data, response_status = TaskComponents.get_task_response(user, id)

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
   