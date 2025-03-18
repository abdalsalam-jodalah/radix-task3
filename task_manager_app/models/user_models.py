from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.db import models
from django.core.exceptions import ValidationError
from .role_models import Role

import logging
logger = logging.getLogger("models")

class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        db_table = '_user'
        ordering = ['-date_joined']
        
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)  
    role = models.ForeignKey(Role, verbose_name=("user role"), on_delete=models.CASCADE, related_name="users")
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_logged_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Account Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")
    parent = models.ForeignKey("User", related_name="sub_users", on_delete=models.SET_NULL, null=True, blank=True)
    username = None  
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    def validate_email(self):
        if not self.email:
            raise ValidationError({"email": "Email is required."})

    def set_full_name_default(self):
        if not self.full_name:
            self.full_name = self.email.split("@")[0]

    def split_full_name(self):
        name_parts = self.full_name.split(" ", 1)
        self.first_name = name_parts[0]
        self.last_name = name_parts[1] if len(name_parts) > 1 else ""

    def hash_password_if_needed(self):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

    def clean(self):
        super().clean()
        self.validate_email()
        self.set_full_name_default()
        self.split_full_name()
        self.hash_password_if_needed()

    def save(self, *args, **kwargs):
        self.full_clean()
        logger.debug(f"Saving User {self.email} with role {self.role}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.email} ({self.role})"
