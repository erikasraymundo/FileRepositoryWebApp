from django.db import models
from category_management.models import Category
from users_management.models import CustomUser

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length = 200)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    customuser_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
