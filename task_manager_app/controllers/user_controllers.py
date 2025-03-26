from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from ..permissions.user_permissions import IsSingleDeviceANDIsAuthenticatedAndUpdateStatus
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 
from ..components.role_permission_components import RolePermissionComponent
logger = logging.getLogger("controllers")
from ..components.auth_components import AuthComponents
from ..models.user_models import User
from ..constants.role_constants import RoleChoices
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
from ..decorators.handle_exceptions import handle_exceptions

class UserApi(APIView):
    pagination_class = CustomPagination
    authentication_classes = []

    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        else:
            return [IsSingleDeviceANDIsAuthenticatedAndUpdateStatus()] 
    
    @handle_exceptions
    def get(self, request, id=None):
        subject_user = AuthComponents.fetch_user_from_req(request)
        users = RolePermissionComponent.handle_action(subject_user, "user", "get")
        if not users:
            return Response(users, status=status.HTTP_200_OK)
        if id:
            user= UserComponents.get_user_from_users(users, id)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(users, request)
        response = paginator.get_paginated_response(UserSerializer(result_page, many=True).data)
        return response
            
        
    @handle_exceptions
    def post(self, request):
        signup_data = AuthComponents.fetch_signup_data_from_req(request)
        signup_data.update({"role": RoleChoices.SUB_USER.value})
        UserComponents.validate_existing_user(signup_data)
        # user = RolePermissionComponent.handle_action(signup_data, "user", "post", request.data)
        # TODO: Fix the dispatcher since it take user object , but here we have data and want to make user obj
        user = UserComponents.create_user(signup_data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    
        
    @handle_exceptions
    def put(self, request, id=None):
        user_id =id
        if user_id == None:
            return Response({"error": "Missing user id, not found."}, status=status.HTTP_400_BAD_REQUEST)
        subject_user = AuthComponents.fetch_user_from_req(request)
        data = request.data
        result = RolePermissionComponent.handle_action(subject_user, "user", "put", data, user_id)
        return Response(UserSerializer(result).data, status=status.HTTP_200_OK)
        
        
    @handle_exceptions
    def patch(self, request, id=None):
        return self.put(request,id)
    
    @handle_exceptions
    def delete(self, request, id=None):
        user_id =id
        if user_id == None:
            return Response({"error": "Missing user id, not found."}, status=status.HTTP_400_BAD_REQUEST)
        subject_user = AuthComponents.fetch_user_from_req(request)
        RolePermissionComponent.handle_action(subject_user, "user", "delete", pk=user_id)
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
    
