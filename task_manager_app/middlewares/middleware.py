import logging
from django.utils import timezone

logger = logging.getLogger("server")  # Adjust logger name based on your logging configuration

class ComprehensiveLoggingMiddleware:
    """
    Middleware that logs request and response details:
      - Timestamp (date and time)
      - HTTP method
      - Full URL (path and query parameters)
      - Client IP address
      - Response status code
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request details
        request_time = timezone.now()
        ip_address = request.META.get("REMOTE_ADDR", "unknown")
        logger.info(
            f"[{request_time}] Request: {request.method} {request.get_full_path()} from {ip_address}"
        )

        # Process the request to get a response
        response = self.get_response(request)

        # Log outgoing response details
        response_time = timezone.now()
        logger.info(
            f"[{response_time}] Response: status {response.status_code} for {request.method} {request.get_full_path()}"
        )
        return response
