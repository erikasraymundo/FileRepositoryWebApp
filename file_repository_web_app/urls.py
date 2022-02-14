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
from users_management.views import profile, UpdatePassword, DeleteAccount, UpdateAccountDetails, ManageAccounts, ArchiveAccounts, AddAccount, EditAccount, ViewAccount, ArchieveUserAccount, RestoreUserAccount
from category_management.views import categoryManagement, AddCategory, UpdateCategory, DeleteCategory, printcategories
from users_management.views import printpdf, printusers, printactivitylogs
from activity_log.views import view_logs
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('file-management/', include('file_management.urls')),
    path('activity-log/', include('activity_log.urls')),
    path('login/', login, name='login'),
    path('registration/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/update-password', UpdatePassword, name='UpdatePassword'),
    path('profile/delete-account', DeleteAccount, name='DeleteAccount'),
    path('profile/update-account', UpdateAccountDetails, name='UpdateAccountDetails'),
    path('manage-accounts/', ManageAccounts, name='ManageAccounts'),
    path('manage-accounts/archived-a-user', ArchieveUserAccount, name='ArchieveUserAccount'),
    path('manage-accounts/restore-a-user', RestoreUserAccount, name='RestoreUserAccount'),
    path('manage-accounts/add-a-user', AddUserAccount, name='AddUserAccount'),
    path('manage-accounts/Add', AddAccount, name='AddAccount'),
    path('manage-accounts/Edit', EditAccount, name='EditAccount'),
    path('manage-accounts/View', ViewAccount, name='ViewAccount'),
    path('manage-accounts/archived', ArchiveAccounts, name='ArchiveAccounts'),
    path('category/', categoryManagement, name='categoryManagement'),
    path('printpdf/', printpdf, name='printpdf'),
    path('printusers/', printusers, name='printusers'),
    path('printcateg/', printcategories, name='print_categ'),
    path('category/add', AddCategory, name='AddCategory'),
    path('category/update', UpdateCategory, name='UpdateCategory'),
    path('category/delete', DeleteCategory, name='DeleteCategory'),
    path('printactivitylogs/', printactivitylogs, name='PrintActivityLogs')]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
