from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = models.PositiveSmallIntegerField()
    middle_name = models.CharField(max_length=200, null=True)
    gender = models.PositiveSmallIntegerField()
    birthdate = models.DateField()
    address = models.CharField(max_length=500)
    profile_picture = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='profile_pics/',max_length=254, null=True)

    def full_name(self):
        return self.first_name + " " + self.last_name
