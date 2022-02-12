from django.db import models
from users_management.models import User

class Log(models.Model):
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
