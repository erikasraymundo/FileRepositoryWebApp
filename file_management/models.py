from django.db import models

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length = 200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
