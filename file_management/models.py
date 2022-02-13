from fileinput import filename
from django.db import models
from category_management.models import Category
from users_management.models import User

# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200)
    url = models.FileField(upload_to='uploads/',max_length=254)
    description = models.CharField(max_length = 200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 

    def getFileUrl(self):
        return self.url.url.replace("\\", "/").replace("/", "\\")

    def getNewFileName(self):
        file_path = self.url.url.replace("_media_uploads_", "")
        index = file_path.rfind('.')
        # file_name = filename[:index]
        file_ex = file_path[index:]
        return self.name + file_ex

    def getFileExtension(self):
        file_path = self.url.url.replace("_media_uploads_", "")
        index = file_path.rfind('.')
        file_ex = file_path[index+1:]
        return file_ex
