from django.shortcuts import render


def profile(request):
    return render(request, 'profile.html')

def manage_accounts(request):
    return render(request, 'manage-accounts.html')

