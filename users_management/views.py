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
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, deleted_at__isnull = True),
    })

def DeleteAccount(request):
    admin = User.objects.get(pk = request.POST['DeleteID'])
    admin.deleted_at = timezone.now()
    admin.updated_at = timezone.now()
    admin.save()
    return render(request, 'profile/profile.html', {
        'details' : User.objects.filter(pk =1, deleted_at__isnull = True),
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
        'details' : User.objects.filter(pk =1, deleted_at__isnull = True),
    })