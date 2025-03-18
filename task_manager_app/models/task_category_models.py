from django.db import models
from django.core.exceptions import ValidationError
import logging
logger = logging.getLogger("models")

class TaskCategory(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = '_category'

    name = models.CharField(max_length=255, default="No name")
    description = models.TextField(max_length=255, default="No description")

    def __str__(self):
        return self.name

    def validate_name(self):
        if not self.name:
            raise ValidationError({"name": "Name is required."})

    def clean(self):
        super().clean()
        self.validate_name()

    def save(self, *args, **kwargs):
        self.full_clean()
        logger.debug(f"Saving Category {self.name}")
        super().save(*args, **kwargs)
