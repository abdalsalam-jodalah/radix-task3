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
