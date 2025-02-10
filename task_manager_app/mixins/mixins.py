import uuid
from django.db import models
from django.utils import timezone
import random

class BaseModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # id = models.BigIntegerField(primary_key=True, default=random.randint(1000000000, 9999999999), editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
