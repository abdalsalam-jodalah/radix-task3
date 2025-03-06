from ..components.user_components import UserComponents
from .base_dispatcher import BaseDispatcher
from ..constants.access_levels import AccessLevel

class UserDispatcher(BaseDispatcher):
    def get(self, subject_user, model, access_level, data=None, pk=None):
        if access_level == AccessLevel.ALL.value:
            return UserComponents.get_all_users()
        elif access_level == AccessLevel.OWN_BELOW.value:
            return UserComponents.get_own_below(subject_user)
        elif access_level == AccessLevel.OWN.value:
            return UserComponents.get_own(subject_user)
        return None

    def post(self, subject_user, model, access_level, data, pk=None):
        return UserComponents.create_user(data)

    def put(self, subject_user, model, access_level, data, pk):
        try:
            print(f"----------in put {subject_user, model, access_level, data, pk}")
            try:
                UserComponents.get_user_by_id(pk)
            except Exception:
                return "User not found!"

            if access_level == AccessLevel.ALL.value:
                return UserComponents.update_user(data, pk)
            elif access_level == AccessLevel.OWN_BELOW.value:
                return UserComponents.put_own_below(subject_user, data, pk)
            elif access_level == AccessLevel.OWN.value:
                return UserComponents.put_own(subject_user, data, pk)
            return None
        except Exception as err:
            print(f"Err in put dispatcher {err}")


    def delete(self, subject_user, model, access_level, data, pk):
        if access_level == AccessLevel.ALL.value:
            return UserComponents.delete_user(pk)
        return None
