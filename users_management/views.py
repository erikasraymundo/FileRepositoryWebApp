from django.shortcuts import render


def profile(request):
    return render(request, 'profile/profile.html')

def manage_accounts(request):
    return render(request, 'user-accounts/manage-accounts.html')

def add_accounts(request):
    return render(request, 'user-accounts/add-account.html')

def edit_accounts(request):
    return render(request, 'user-accounts/edit-account.html')

def archive_accounts(request):
    return render(request, 'user-accounts/archive-account.html')

