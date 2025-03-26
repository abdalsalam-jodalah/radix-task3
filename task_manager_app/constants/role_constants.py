from django.db import models

class RoleChoices(models.Choices):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"
    SUB_USER ="sub_user"

class RoleMap(models.Choices):
    ADMIN = "1"
    MANAGER = "2"
    USER = "3"
    SUB_USER ="4"