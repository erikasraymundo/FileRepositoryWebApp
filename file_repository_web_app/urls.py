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
from accounts.views import login
from accounts.views import register
from users_management.views import profile
from users_management.views import manage_accounts
from category_management.views import categoryManagement
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file-management/', include('file_management.urls')),
    path('login/', login, name='login'),
    path('registration/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('manage-accounts/', manage_accounts, name='manage_accounts'),
    path('category/', categoryManagement, name='categoryManagement'),
]
