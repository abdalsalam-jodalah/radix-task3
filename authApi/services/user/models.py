from django.db import models
from authApi.mixins import BaseModelMixin
from django.contrib.auth.hashers import make_password, check_password

class User(BaseModelMixin):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'user_table'
        ordering = ['-created_at']
        
    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        USER = "user"

    role = models.CharField(max_length=5, choices= RoleChoices, default=RoleChoices.USER)
    name = models.CharField(max_length=255)
    username = models.CharField(unique=True)
    password = models.CharField(max_length=255)
    isLoggedIn = models.BooleanField(default=False)

    def __str__(self):
        return f"Book: {self.title}"
    
    def save(self, *args, **kwargs):
        if self.password:
            self.password = make_password(self.password)  
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  

    