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
        
    id = models.AutoField(editable=False, primary_key=True)
    email = models.EmailField(unique=True)  
    role = models.ForeignKey(Role, verbose_name=("user role"), on_delete=models.CASCADE, related_name="users")
    is_logged_in = models.BooleanField(default=False)
    created_at = models.DateTimeField(editable=False, auto_now_add=True, verbose_name="Account Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Last Updated At")
    parent = models.ForeignKey("User", related_name="sub_users", on_delete=models.SET_NULL, null=True, blank=True)
    username = None  
    last_login = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def validate_email(self):
        if not self.email:
            raise ValidationError({"email": "Email is required."})

        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                raise ValidationError({"email": "Email is already in use."})
        

    def hash_password_if_needed(self):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
    
    def validate_role(self):
        # if self.role.name == "admin":
        #     raise ValidationError({"role":"User cannot be assigned admin role."})
        
        if self.role.name and self.role.name not in Role.objects.values_list("name", flat=True):
            raise ValidationError({"role":"Role does not exist."})

    def clean(self):
        super().clean()
        self.validate_email()
        self.hash_password_if_needed()
        self.validate_role()

    def save(self, *args, **kwargs):
        self.full_clean()
        logger.debug(f"Saving User {self.email} with role {self.role}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.email} ({self.role})"
    
