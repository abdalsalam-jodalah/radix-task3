from django.db import models
import uuid

class BaseModelMixin(models.Model):
    # id = models.AutoField(editable=False, primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
