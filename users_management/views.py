from django.shortcuts import render
from datetime import datetime
from .models import User
from django.utils import timezone

def profile(request):
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, deleted_at__isnull = True),
    })

def UpdatePassword(request):
    admin = User.objects.get(pk = 1)
    admin.password = request.POST['newPassword']
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def DeleteAccount(request):
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def UpdateAccountDetails(request):
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.updated_at = timezone.now()
    admin.username = request.POST['username']
    admin.first_name = request.POST['first_name']
    admin.last_name = request.POST['last_name']
    admin.address = request.POST['address']
    admin.email = request.POST['email']
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, is_active = 1),
    })

def ManageAccounts(request):
    return render(request, 'user-accounts/manage-accounts.html', {
        'users' : User.objects.filter(is_active = 1),
    })

def ArchiveAccounts(request):
    return render(request, 'user-accounts/archive-account.html', {
        'users' : User.objects.filter(is_active = 0),
    })

def AddAccount(request):
    list = []
    users = User.objects.all()
    for user in users:
        list.append(user.username)
    
    return render(request, 'user-accounts/add-account.html', {
        'users' : User.objects.all(),
        'username' : list,
    })

def AddUserAccount(request):
    user = User()
    user.username = request.POST['username']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.middle_name = request.POST['middle_name']
    user.address = request.POST['address']
    user.email = request.POST['email']
    user.gender = request.POST['group']
    birthdate = request.POST['birthday']
    user.birthdate = datetime(int(birthdate[6:10]), int(birthdate[0:2]), int(birthdate[3:5]))
    user.date_joined =  timezone.now()
    user.is_superuser = False
    user.is_staff = False
    user.user_type = 1
    user.save()
    return render(request, 'user-accounts/manage-accounts.html', {
        'users' : User.objects.filter(is_active = 1),
    })
    
def EditAccount(request):
    return render(request, 'user-accounts/edit-account.html', {
        'users' : User.objects.filter(pk = request.POST['PK']),
    })

def ViewAccount(request):
    return render(request, 'user-accounts/view-account.html', {
        'users' : User.objects.filter(pk = request.POST['PK']),
    })

def ArchieveUserAccount(request):
    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = False
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'user-accounts/archive-account.html', {
        'users' : User.objects.filter(is_active = 0),
    })

def RestoreUserAccount(request):
    admin = User.objects.get(pk = request.POST['ID'])
    admin.is_active = True
    admin.deleted_at = None
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'user-accounts/manage-accounts.html', {
        'users' : User.objects.filter(is_active = 1),
    })