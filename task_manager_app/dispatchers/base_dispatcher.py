class BaseDispatcher:
    def get(self, user, model, access_level,data=None, pk=None):
        # Process the `get` action with 3 parameters
        pass

    def post(self, user, model, access_level, data,pk=None):
        # Process the `post` action with 4 parameters
        pass

    def put(self, user, model, access_level, data=None,pk=None):
        # Process the `put` action with 4 parameters
        pass

    def delete(self, user, model, access_level, data=None, pk=None):
        # Process the `delete` action with 4-5 parameters
        pass
