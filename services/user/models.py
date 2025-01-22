from django.db import models
from authApi.mixins import BaseModelMixin
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.core.exceptions import ValidationError

class User(BaseModelMixin):# id , craeted_at, updeted_at
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
    username = models.CharField(max_length=255,unique=True) #email
    password = models.CharField(max_length=255)
    isLoggedIn = models.BooleanField(default=False)
    
    @property
    def last_login_from(self):
        return  timezone.now() - self.updated_at

    # def __str__(self):
    #     return f"user name: {self.username} | name: {self.name} | role: {self.role} |isLoggedIn: {self.isLoggedIn} "
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        if User.objects.filter(username=self.username):
        # if User.objects.filter(username=self.username).exclude(id=self.id).exists():
            raise ValidationError("Email is already in use!")
        super().save(*args, **kwargs)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  
    
