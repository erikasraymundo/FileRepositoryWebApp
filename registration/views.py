from django.shortcuts import render


def registration_page(request):
    return render(request, 'registration.html')