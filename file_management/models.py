from django import template
from fileinput import filename
from django.db import models
from category_management.models import Category
from users_management.models import User

import os
# Create your models here.

class File(models.Model):
    name = models.CharField(max_length=200)
    url = models.FileField(upload_to='uploads/',max_length=254)
    description = models.TextField(null=True)
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

    def getSize(self):
        value = self.url.size
        if value < 512000:
            value = value / 1024.0
            ext = 'kb'
        elif value < 4194304000:
            value = value / 1048576.0
            ext = 'mb'
        else:
            value = value / 1073741824.0
            ext = 'gb'
        return '%s %s' % (str(round(value, 2)), ext)

    def getAbsolutePath(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        return BASE_DIR + self.getFileUrl()

    def getFileType(self):
        file_ext = self.getFileExtension()
        images = ('jpg', 'jpeg', 'gif', 'png', 'webp')
        videos = ('mpeg', 'mp4', 'ogg', 'mkv')
        if file_ext in images:
            return 1
        elif file_ext in videos:
            return 2
        elif file_ext == 'pdf':
            return 3
        else:
            return 4
