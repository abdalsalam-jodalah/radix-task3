from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..permissions.user_permissions import IsSingleDevice
from ..serializers.user_serializers import UserSerializer
from ..components.user_components import UserComponents
from ..components.shared_components import SharedComponents
from ..pagination import CustomPagination
import logging 

logger = logging.getLogger("views")

class RoleApi(APIView):
        def get (self, request, pk=None):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        def post (self, request):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
        def put (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
        def patch (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        def delete (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)

class PermissionApi(APIView):
        def get (self, request, pk=None):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        def post (self, request):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
        def put (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
    
        def patch (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
        
        def delete (self, request, pk):
            try:
                logger.debug(SharedComponents.get_log_message("UserApi", "GET", None, None, "User", "listing roles"))
            except Exception as e:  
                logger.error(SharedComponents.get_log_message("RoleApi", "GET", None, None, "User", f"Validation error: {e.with_traceback(e.__traceback__)}"))
                return Response({"error": f"Invalid request:  {e}"}, status=status.HTTP_400_BAD_REQUEST)
