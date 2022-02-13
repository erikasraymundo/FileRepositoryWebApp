from django.shortcuts import render


def profile(request):
    return render(request, 'profile/profile.html')

def manage_accounts(request):
    return render(request, 'user-accounts/manage-accounts.html')

