from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotAcceptable

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 
from ..permissions.auth_permissions import IsAuthenticatedAndUpdateStatus
from ..components.role_permission_components import RolePermissionComponent
logger = logging.getLogger("controllers")
from ..components.auth_components import AuthComponents
from ..models.user_models import User
from ..constants.role_constants import RoleChoices
from django.core.exceptions import ValidationError

class UserApi(APIView):
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'POST':
            return [] 
        else:
            # return [IsAuthenticatedAndUpdateStatus(), IsSingleDevice()] 
            # return [IsSingleDevice()] 
            return [] 


    def get(self, request, id=None):
        try:
            subject_user = AuthComponents.fetch_user_from_req(request)
            users = RolePermissionComponent.handle_action(subject_user, "user", "get")

            if id:
                if not isinstance(id,int):
                    return Response({"error": "User not found!, or don't You have permissions"}, status=status.HTTP_404_NOT_FOUND) 
                user= UserComponents.get_user_from_users(users, id)
                if not user:
                    return Response({"error": "User not found!, or don't You have permissions"}, status=status.HTTP_404_NOT_FOUND)   
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

            paginator = CustomPagination()
            result_page = paginator.paginate_queryset(users, request)
            response = paginator.get_paginated_response(UserSerializer(result_page, many=True).data)
            return response
            
        except ValueError:
            raise ValidationError("The provided id must be an integer.")
        except NotAcceptable as err:
            return Response({"error": str(err)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            signup_data = AuthComponents.fetch_signup_data_from_req(request)
            signup_data.update({"role": RoleChoices.SUB_USER.value})
            UserComponents.validate_existing_user(signup_data)
            # user = RolePermissionComponent.handle_action(signup_data, "user", "post", request.data)
            # TODO: Fix the dispatcher since it take user object , but here we have data and want to make user obj
            user = UserComponents.create_user(signup_data)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        try:
            user_id =id
            if user_id == None:
                return Response({"error": "Missing user id, not found."}, status=status.HTTP_400_BAD_REQUEST)
            subject_user = AuthComponents.fetch_user_from_req(request)
            data = request.data
            result = RolePermissionComponent.handle_action(subject_user, "user", "put", data, user_id)
            return Response(UserSerializer(result).data, status=status.HTTP_200_OK)
        
        except ValueError:
            raise ValidationError("The provided id must be an integer.")
        except NotAcceptable as err:
            return Response({"error": str(err)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except User.DoesNotExist as ert:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred.{e}"}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        return self.put(request,id)

    def delete(self, request, user_id):
        """Delete a user"""
        logger.debug(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "Deleting user"))
        subject_user = AuthComponents.get_user(request)
        if not subject_user or not isinstance(subject_user, User):
            return Response({"error": "Invalid token or user not found."}, status=status.HTTP_400_BAD_REQUEST)
            
        user = UserComponents.get_user_by_id(user_id)
        if not user:
            logger.warning(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User not found"))
            return Response({"error": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        logger.info(SharedComponents.get_log_message("UserApi", "DELETE", request.user, user_id, "User", "User deleted successfully"))
        return Response({"message": "User deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
