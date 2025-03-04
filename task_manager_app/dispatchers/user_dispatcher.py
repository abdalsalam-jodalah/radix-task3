from ..components.user_components import UserComponents
from .base_dispatcher import BaseDispatcher
from constants.access_levels import AccessLevel
class UserDispatcher(BaseDispatcher):
    def get(self, user, model, access_level, data=None, pk=None):
        if access_level == AccessLevel.ALL.value:
             pass
        elif access_level == AccessLevel.OWN_BELOW:
            pass
        elif access_level == AccessLevel.OWN:
            pass
        return None 
    
    def post(self, user, model, access_level, data, pk=None):
        if access_level == AccessLevel.ALL.value:
            pass
        if access_level == AccessLevel.OWN_BELOW:
            pass
        if access_level == AccessLevel.OWN:
            pass
        return None
    
    def put(self, user, model, access_level, data, pk):
        if access_level == AccessLevel.ALL.value:
            pass
        elif access_level == AccessLevel.OWN_BELOW:
            pass
        elif access_level == AccessLevel.OWN:
            pass
        return None
        
    def delete(self, user, model, access_level, data, pk):
        if access_level ==AccessLevel.ALL.value:
            pass
        return None
