from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    user_type = models.PositiveSmallIntegerField()
    middle_name = models.CharField(max_length=200)
    gender = models.PositiveSmallIntegerField()
    birthdate = models.DateField()
    address = models.CharField(max_length=500)
    profile_picture = models.CharField(max_length=500)
    created_at = models.DateField()
    updated_at = models.DateField()
    deleted_at = models.DateField()

