from django.shortcuts import render
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
    return render(request, 'user-accounts/add-account.html', {
        'users' : User.objects.all(),
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