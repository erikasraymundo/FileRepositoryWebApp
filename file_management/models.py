from django.db import models
from category_management.models import Category
from users_management.models import User

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    description = models.CharField(max_length = 200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
