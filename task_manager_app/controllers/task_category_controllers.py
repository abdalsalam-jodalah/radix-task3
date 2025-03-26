from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..permissions.user_permissions import IsSingleDeviceANDIsAuthenticatedAndUpdateStatus
from ..pagination import CustomPagination
from ..components.task_category_components import TaskCategoryComponents
from ..serializers.task_category_serializers import TaskCategorySerializer
from ..decorators.handle_exceptions import handle_exceptions

import logging
logger = logging.getLogger("controllers")

class TaskCategoryApi(APIView):
    authentication_classes = []

    permission_classes = [ IsSingleDeviceANDIsAuthenticatedAndUpdateStatus]
    pagination_class = CustomPagination
    
    @handle_exceptions      
    def get(self, request, pk=None):
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

   
    @handle_exceptions   
    def post(self, request):
        serializer = TaskCategorySerializer(data=request.data)
        if serializer.is_valid():
            
                category = TaskCategoryComponents.create_category(serializer.validated_data)
                return Response(TaskCategorySerializer(category).data, status=status.HTTP_201_CREATED)
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
    @handle_exceptions   
    def put(self, request, pk=None):
        updated_category = TaskCategoryComponents.update_category(pk, request.data)
        if not updated_category:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskCategorySerializer(updated_category)
        return Response(serializer.data, status=status.HTTP_200_OK)

   
    @handle_exceptions   
    def patch(self, request, pk):
        updated_category = TaskCategoryComponents.update_category(pk, request.data)
        if not updated_category:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TaskCategorySerializer(updated_category)
        return Response(serializer.data, status=status.HTTP_200_OK)

   
    @handle_exceptions   
    def delete(self, request, pk):
        success = TaskCategoryComponents.delete_category(pk)
        if not success:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Category deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

