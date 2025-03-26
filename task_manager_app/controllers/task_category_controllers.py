from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.user_permissions import IsSingleDeviceANDIsAuthenticatedAndUpdateStatus
from ..pagination import CustomPagination
from ..components.task_category_components import TaskCategoryComponents
from ..serializers.task_category_serializers import TaskCategorySerializer

import logging
logger = logging.getLogger("controllers")

class TaskCategoryApi(APIView):
    authentication_classes = []

    permission_classes = [ IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]
    pagination_class = CustomPagination

    def get(self, request, pk=None):
        try:
            if pk:
                category = TaskCategoryComponents.get_category(pk)
                if not category:
                    return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
                serializer = TaskCategorySerializer(category)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                categories = TaskCategoryComponents.get_all_categories()
                paginator = self.pagination_class()
                page = paginator.paginate_queryset(categories, request, view=self)
                if page is not None:
                    serializer = TaskCategorySerializer(page, many=True)
                    return paginator.get_paginated_response(serializer.data)
                else:
                    serializer = TaskCategorySerializer(categories, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching categories: {e}")
            return Response({"detail": f"An error occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = TaskCategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                category = TaskCategoryComponents.create_category(serializer.validated_data)
                return Response(TaskCategorySerializer(category).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"Error creating category: {e}")
                return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        try:
            
            updated_category = TaskCategoryComponents.update_category(pk, request.data)
            if not updated_category:
                return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskCategorySerializer(updated_category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            return Response({"detail": f"An error occurred {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            updated_category = TaskCategoryComponents.update_category(pk, request.data)
            if not updated_category:
                return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = TaskCategorySerializer(updated_category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error updating category: {e}")
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            success = TaskCategoryComponents.delete_category(pk)
            if not success:
                return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            logger.error(f"Error deleting category: {e}")
            return Response({"detail": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
