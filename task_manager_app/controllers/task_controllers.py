
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.user_permissions import IsSingleDevice
from ..pagination import CustomPagination
from ..components.auth_comopnents import AuthComponents as AC
from ..components.task_components import TaskComponents
from ..serializers.task_serializers import TaskSerializer
import logging 

logger = logging.getLogger("views")

class TaskApi(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSingleDevice]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        if pk:
            task, response_data, response_status = TaskComponents.get_task_response(user, pk)
            if task is None:
                return Response(response_data, status=response_status)
            return Response(response_data, status=response_status)

        tasks = TaskComponents.get_tasks_for_user(user)
        paginated_tasks = self.pagination_class().paginate_queryset(tasks, request)
        serializer = TaskSerializer(paginated_tasks, many=True)

        return self.pagination_class().get_paginated_response(serializer.data)

    def post(self, request):
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        response_data, response_status = TaskComponents.create_task(user, request.data)
        return Response(response_data, status=response_status)

    def put(self, request, pk=None):
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        response_data, response_status = TaskComponents.update_task(user, pk, request.data)
        return Response(response_data, status=response_status)

    def delete(self, request, pk=None):
        user = AC.get_user(request)
        if not user:
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)

        response_data, response_status = TaskComponents.delete_task(user, pk)
        return Response(response_data, status=response_status)
