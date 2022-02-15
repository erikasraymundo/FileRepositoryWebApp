from os import remove
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def loginView(request):
    return render(request, 'accounts/login.html')

# need po itong baguhin
def login(request):
    setupSession(request, 2, False)
    return HttpResponseRedirect(reverse('file-management:index'))


def registerView(request):
    return render(request, 'accounts/registration.html')

# need po itong baguhin
def register(request):
    setupSession(request, 2, False)
    return HttpResponseRedirect(reverse('login'))

def logout(request):
    removeSession(request)
    return HttpResponseRedirect(reverse('loginView'))

def setupSession(request, user_id, is_superuser):
    request.session['user_id'] = user_id
    request.session['is_superuser'] = is_superuser

def removeSession(request):
    del request.session['user_id']
    del request.session['is_superuser']
