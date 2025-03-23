import logging

logger = logging.getLogger('controllers')

class RequestResponseLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log incoming request details
        logger.info(f"Request: {request.method} {request.get_full_path()}")
        # Optionally, log headers or even the body (if safe)
        # logger.debug(f"Request headers: {request.headers}")
        # logger.debug(f"Request body: {request.body}")

        response = self.get_response(request)
        
        # Log outgoing response details
        logger.info(f"Response status: {response.status_code}")
        # Optionally, log response headers or content
        # logger.debug(f"Response headers: {response.items()}")
        # logger.debug(f"Response body: {response.content}")

        return response
