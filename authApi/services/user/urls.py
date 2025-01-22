from django.urls import path, include

urlpatterns= [
    path("signup/", name="signup"),
    path("login/", name="login"),
    path(" ",  name="list_users"),
    path("/<int:user_id> ",  name="list_users"),
    path("edit/", name="")
]