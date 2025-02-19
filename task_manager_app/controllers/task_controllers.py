
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.user_permissions import IsSingleDevice
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..pagination import CustomPagination
from ..components.auth_comopnents import AuthComponents as AC
from ..components.task_components import TaskComponents
from ..serializers.task_serializers import TaskSerializer
from ..models.email_notification_model import EmailNotification
from ..components.task_notification import send_task_notification
from ..models.user_models import User
from ..models.task_models import Task
import logging 

logger = logging.getLogger("views")

class TaskApi(APIView):
    authentication_classes = []
    permission_classes = [IsAuthenticatedAndUpdateStatus, IsSingleDevice]
    pagination_class = CustomPagination
    def get(self, request, pk=None):
        print( f"pk: {pk}") 

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
            print(f"filters: {filters}")
            tasks, response_status = TaskComponents.get_tasks_assigned_for_user(user, filters)
            if tasks is None:
                return Response(response_status, status=status.HTTP_404_NOT_FOUND)
            paginator = self.pagination_class()
            paginated_tasks = paginator.paginate_queryset(tasks, request)
            
            if paginated_tasks is None:
                return Response({"error": "No tasks available for the given filters."}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(paginated_tasks, many=True)
            return paginator.get_paginated_response(serializer.data)

            paginated_tasks = self.pagination_class().paginate_queryset(tasks, request)
            serializer = TaskSerializer(paginated_tasks, many=True)

            return self.pagination_class().get_paginated_response(serializer.data)
        except Exception as e:
            logger.error(f"Error getting task: {e.with_traceback( e.__traceback__)}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try: 
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            data = TaskComponents.fetch_user_data(request)
            task, response_status = TaskComponents._handle_create_task(user=user, data=data)

            if task and task.name:
                notification = EmailNotification.objects.create(
                    user=user,
                    message=f"You have been assigned a new task: {task.name}",
                    task=task
                )
                print(f"notification: {notification}")
                send_task_notification.delay(notification.id)
                return Response( {"task": TaskSerializer(task).data}, status.HTTP_201_CREATED )
            
            status_code = response_status.get("status") if isinstance(response_status, dict) else 400
            return Response(
                {"task": TaskSerializer(task).data} if task else {"error": "Invalid request"},
                status=int(status_code)
            )
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk=None):
        try:
            user = AC.get_user(request)
            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

            response_data, response_status = TaskComponents.update_task(user, pk, request.data)
            return Response(response_data, status=response_status)
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request, pk=None):
        try:
            user = AC.get_user(request)

            if not user or not isinstance(user, User):
                return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

            response_data, response_status = TaskComponents.delete_task(user, pk)
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
            print(f"tasks: {tasks}")
            
            paginator = self.pagination_class()
            paginated_tasks = paginator.paginate_queryset(tasks, request)
            
            if paginated_tasks is None:
                return Response({"error": "No tasks available for the given filters."}, status=status.HTTP_404_NOT_FOUND)

            serializer = TaskSerializer(paginated_tasks, many=True)
            return paginator.get_paginated_response(serializer.data)




            paginated_tasks = self.pagination_class().paginate_queryset(tasks, request)
            serializer = TaskSerializer(paginated_tasks, many=True)
            print(f"filters: {filters}")

            return self.pagination_class().get_paginated_response(serializer.data)
        except Exception as e:  
            logger.error(f"Error getting task: {e}")
            return Response({"error": f"Invalid request:  {e} \n{e.with_traceback(e.__traceback__)}"}, status=status.HTTP_400_BAD_REQUEST)
