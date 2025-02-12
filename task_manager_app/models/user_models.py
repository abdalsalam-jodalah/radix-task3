from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from django.db import models
import logging

logger = logging.getLogger("models")

class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = '_user'
        ordering = ['-date_joined']
        
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    email = models.EmailField(unique=True)  
    role = models.CharField(max_length=5, choices=RoleChoices.choices, default=RoleChoices.USER)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_logedin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  

    def save(self, *args, **kwargs):
        """Custom save method with logging and security improvements."""
        if not self.username:
            self.username = f"user_{get_random_string(8)}"

        if not self.full_name:
            self.full_name = self.email.split("@")[0]

        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        logger.debug(f"Saving user {self.email} with role {self.role}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"

    def set_login_status(self, status: bool):
        """Helper method to update login status with logging."""
        self.is_logedin = status
        self.save()
        logger.info(f"User {self.email} login status updated to {status}")

