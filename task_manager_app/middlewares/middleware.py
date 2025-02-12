import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("request_logger")

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info(f"Request: {request.method} {request.path} from {request.META.get('REMOTE_ADDR')}")
import logging

logger = logging.getLogger("requests")

class RequestLoggerMiddleware:
    """Middleware to log incoming requests."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"Request: {request.method} {request.path}")
        response = self.get_response(request)
        return response 
