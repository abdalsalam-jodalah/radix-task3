from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, PermissionDenied

from ..permissions.user_permissions import IsSingleDevice
from ..pagination import CustomPagination
from ..models.task_models import Task
from ..serializers.task_serializers import TaskSerializer
from ..components.shared_components import SharedComponents as SC
from ..components.auth_comopnents import AuthComponents as AC
import logging 

logger = logging.getLogger("views")


class TaskApi(APIView):
    """
    Handles CRUD operations for tasks.
    - Admin can manage all tasks.
    - Users can only manage their own tasks.
    """
    permission_classes = [permissions.IsAuthenticated, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        """
        GET all tasks (Admin) or user's own tasks.
        If `pk` is provided, return a single task.
        """
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(SC.get_log_message('GET', user, pk, "Requested tasks"))

        if pk:
            try:
                task = Task.objects.get(pk=pk)
                logger.info( SC.get_log_message('GET', user, pk, "Task found"))

                if user.role != "admin" and task.user != user: 
                    logger.warning(SC.get_log_message('GET', user, pk, "Permission denied: Cannot view other user's task"))
                    raise PermissionDenied("You can only view your own tasks.")

                serializer = TaskSerializer(task)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Task.DoesNotExist:
                logger.error(SC.get_log_message('GET', user, pk, "Task not found"))
                return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        tasks = Task.objects.all() if user.role == "admin" else Task.objects.filter(user=user)
        paginated_tasks = self.pagination_class().paginate_queryset(tasks, request)

        logger.debug(SC.get_log_message('GET', user, additional_info=f"Returning {len(paginated_tasks)} tasks"))

        serializer = TaskSerializer(paginated_tasks, many=True)
        return self.pagination_class().get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new task.
        """
        user = AC.get_user(request)
        if not user:
            logger.debug(SC.get_log_message('POST', user, additional_info=f"Creating a new task with data: {request.data}"))
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                task = serializer.save(user=user)
                logger.info(SC.get_log_message('POST', user, task.id, "Task created successfully"))
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.error(SC.get_log_message('POST', user, additional_info=f"Validation Error: {str(e)}"))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.critical(SC.get_log_message('POST', user, additional_info=f"Unexpected Error: {str(e)}"))
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """
        Update a task.
        Admin can update any task.
        Users can only update their own tasks.
        """
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(SC.get_log_message('PUT', user, pk, f"Updating task with data: {request.data}"))

        try:
            task = Task.objects.get(pk=pk)
            logger.info( SC.get_log_message('PUT', user, pk, "Task found for update"))

            if user.role != "admin" and task.user != user:
                logger.warning(SC.get_log_message('PUT', user, pk, "Permission denied: Cannot update other user's task"))
                raise PermissionDenied("You can only update your own tasks.")

            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(SC.get_log_message('PUT', user, pk, "Task updated successfully"))
                return Response(serializer.data, status=status.HTTP_200_OK)

        except Task.DoesNotExist:
            logger.error(SC.get_log_message('PUT', user, pk, "Task not found"))
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            logger.error(SC.get_log_message('PUT', user, pk, f"Validation Error: {str(e)}"))
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.critical(SC.get_log_message('PUT', user, pk, f"Unexpected Error: {str(e)}"))
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        """
        Delete a task.
        Admin can delete any task.
        Users can only delete their own tasks.
        """
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Token not valid or user not found."}, status=status.HTTP_400_BAD_REQUEST)
        logger.debug(SC.get_log_message('DELETE', user, pk, "Deleting task"))

        try:
            task = Task.objects.get(pk=pk)
            logger.info(SC.get_log_message('DELETE', user, pk, "Task found for deletion"))

            if user.role != "admin" and task.user != user:
                logger.warning( SC.get_log_message('DELETE', user, pk, "Permission denied: Cannot delete other user's task"))
                raise PermissionDenied("You can only delete your own tasks.")

            task.delete()
            logger.info(SC.get_log_message('DELETE', user, pk, "Task deleted successfully"))
            return Response({"detail": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Task.DoesNotExist:
            logger.error(SC.get_log_message('DELETE', user, pk, "Task not found"))
            return Response({"detail": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            logger.critical(SC.get_log_message('DELETE', user, pk, f"Unexpected Error: {str(e)}"))
            return Response({"detail": f"Error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
