from ..models.user_models import User

class UserRepository():
    def fetch_all_users():
        return User.objects.all()
    
    def fetch_user_by_id(user_id):
        return User.objects.get(id=user_id)
    
    def fetch_user_by_username(username):
       return User.objects.get(username=username)    
    
    def create_user(user_data):
        user= User(**user_data)
        user.save()
    
    def update_user(user,user_data):
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()
 