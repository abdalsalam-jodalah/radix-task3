from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password  
from django.utils.crypto import get_random_string


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin"
        USER = "user"

    role = models.CharField(max_length=5, choices=RoleChoices.choices, default=RoleChoices.USER)
    name = models.CharField(max_length=255)
    username = models.EmailField(unique=True)  # Email used for login
    password = models.CharField(max_length=255)
    is_logedin= models.BooleanField(default=False)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = 'user_table'
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        if not self.username:  
            self.username = f"user_{get_random_string(8)}@gmail.com"
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
