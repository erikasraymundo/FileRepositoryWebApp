"""file_repository_web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login.views import login_page
from registration.views import registration_page
from file_management.views import file_management
from users_management.views import profile
from users_management.views import manage_accounts
from users_management.views import category_management
from file_management.views import upload_file

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_page, name='login_page'),
    path('registration/', registration_page, name='registration_page'),
    path('file-management/', file_management, name='file_management'),
    path('profile/', profile, name='profile'),
    path('manage-accounts/', manage_accounts, name='manage_accounts'),
    path('category-management/', category_management, name='category_management'),
    path('upload/', upload_file, name='upload_file'),
]
