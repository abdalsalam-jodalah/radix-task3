from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password  
from django.utils.crypto import get_random_string
from django.core.exceptions import ValidationError

import logging
logger = logging.getLogger("models")

class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = '_user'
        ordering = ['-date_joined']
    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        USER = "user"
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    role = models.CharField(max_length=5, choices=RoleChoices.choices, default=RoleChoices.USER)
    full_name = models.CharField(max_length=255)
    is_logedin= models.BooleanField(default=False)
    username = models.EmailField(unique=True)  # Email used for login
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = f"user_{get_random_string(8)}@gmail.com"
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"

class UserDevice(models.Model):
    class Meta:
        db_table = "_user_devices"  
        
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    is_active = models.BooleanField(default=True)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    device_name = models.CharField(max_length=255, blank= True, default="Unknown Device")
    device_type = models.CharField(max_length=100,  default="Unknown Type")  
    device_token = models.CharField(max_length=255, unique=True)  
   

    def __str__(self):
        return f"{self.device_name} - {self.device_type} ({'Active' if self.is_active else 'Inactive'})"
    
    def clean(self):
        if not self.device_token or len(self.device_token) < 20:
            raise ValidationError("Invalid device token.")
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
