from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()