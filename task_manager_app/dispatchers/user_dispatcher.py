from ..components.user_components import UserComponents
from .base_dispatcher import BaseDispatcher
from ..constants.access_levels import AccessLevel
from django.core.exceptions import ValidationError

class UserDispatcher(BaseDispatcher):
    def get(self, subject_user, model, access_level, data=None, pk=None):
        if access_level == AccessLevel.ALL.value:
            return UserComponents.get_all_users()
        elif access_level == AccessLevel.OWN_BELOW.value:
            return UserComponents.get_own_below(subject_user)
        elif access_level == AccessLevel.OWN.value:
            return UserComponents.get_own(subject_user)
        
        raise ValidationError({"error": "Invalid access level"})
    def post(self, subject_user, model, access_level, data, pk=None):
        return UserComponents.create_user(data)

    def put(self, subject_user, model, access_level, data, pk):
        try:
            UserComponents.get_user_by_id(pk)
    
            if access_level == AccessLevel.ALL.value:
                return UserComponents.update_user(subject_user, data, pk)
            elif access_level == AccessLevel.OWN_BELOW.value:
                return UserComponents.put_own_below(subject_user, data, pk)
            elif access_level == AccessLevel.OWN.value:
                return UserComponents.put_own(subject_user, data, pk)
            
            raise ValidationError({"error": "Invalid access level"})
        except Exception as err:
            raise err

    def delete(self, subject_user, model, access_level, data, pk):
        if access_level == AccessLevel.ALL.value:
            return UserComponents.delete_user(pk)
        raise ValidationError({"error": "Invalid access level"})
