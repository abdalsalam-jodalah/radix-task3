from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotAcceptable, AuthenticationFailed
from django.core.exceptions import ValidationError
from ..models.user_device_models import UserDevice
from ..models.user_models import User
def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except NotAcceptable as err:
            return Response({"error": str(err)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        except ValidationError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AuthenticationFailed as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except AttributeError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except UserDevice.DoesNotExist as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist as err:
            return Response({"error": str(err)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {e}"}, status=status.HTTP_400_BAD_REQUEST)
    return wrapper
