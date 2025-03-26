import logging

logger = logging.getLogger("views")


class SharedComponents:
    @staticmethod
    def get_log_message(api_name, action, user, target_id=None, target_label="Target", additional_info=""):
        """
        Generalized formatter function for creating dynamic log messages across different APIs.
    
        """
        message = f"[{api_name}][{action}] User {user.id if user else 'Anonymous'} - {additional_info}"
        if target_id:
            message += f" - {target_label} {target_id}"
        return message

    @staticmethod
    def log_message(class_name, method, message):
        logger.debug(f"{class_name} - {method}: {message}")
    
    @staticmethod
    def log_error(class_name, method, error):
        logger.error(f"{class_name} - {method}: {error}")
