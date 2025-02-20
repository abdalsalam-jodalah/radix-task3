from django.db import models

class TaskCategory(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        db_table = 'category'

    name = models.CharField(max_length=255, default="No name")
    description = models.TextField(max_length=255, default="No description")

    def __str__(self):
        return self.name
