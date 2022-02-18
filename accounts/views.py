from math import lgamma
from os import remove
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users_management.models import User
from activity_log.models import Log
import datetime
from django.utils import timezone

def loginView(request, error = 0):
    session_user_id = request.session.get('user_id')
    if (session_user_id != None):
        return HttpResponseRedirect(reverse('file-management:index'))

    return render(request, 'accounts/login.html', {"error": error})

# need po itong baguhin
def login(request):
    session_user_id = request.session.get('user_id')
    if (session_user_id != None):
        return HttpResponseRedirect(reverse('file-management:index'))

    usernameEmail = request.POST['usernameEmail']
    password = request.POST['password']

    userUsername = User.objects.filter(
        username__iexact=usernameEmail, password=password).first()
    userEmail = User.objects.filter(
        email__iexact=usernameEmail, password=password).first()


    if userUsername != None:
        user = userUsername

        if user.is_active == 0:
            return render(request, 'accounts/login.html', {"error": 2, "usernameEmail" : user})
        else:
            setupSession(request, user.id, user.is_superuser)

    elif userEmail != None:
        user = userEmail
        if user.is_active == 0:
            return render(request, 'accounts/login.html', {"error": 2, "usernameEmail" : user})
        else:
            setupSession(request, user.id, user.is_superuser)
    else:
        return render(request, 'accounts/login.html', {"error": 1, "usernameEmail" : usernameEmail})

    log = Log()
    log.user_id = User.objects.get(pk=user.id)
    log.description = f'{user.full_name()} ({user.id} - {user.username}) has logged in.'
    log.save()

    return HttpResponseRedirect(reverse('file-management:index'))


def registerView(request, error=0, success=0):
    session_user_id = request.session.get('user_id')
    if (session_user_id != None):
        return HttpResponseRedirect(reverse('file-management:index'))
    return render(request, 'accounts/registration.html', {"error": error, "success" : success})

# need po itong baguhin
def register(request):
    session_user_id = request.session.get('user_id')
    if (session_user_id != None):
        return HttpResponseRedirect(reverse('file-management:index'))

    username = request.POST['username']
    email = request.POST['email']
    userUsername = User.objects.filter(
        username__iexact=username).first()
    userEmail = User.objects.filter(
        email__iexact=email).first()

    user = User()
    user.username = request.POST['username']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.middle_name = request.POST['middle_name']
    user.address = request.POST['address']
    user.email = request.POST['email']
    user.gender = request.POST['gender']
    user.birthdate = request.POST['birthday']
    user.date_joined = timezone.now()
    user.password = request.POST['password']
    user.is_superuser = False
    user.is_staff = False
    user.user_type = 1

    if userUsername != None:
        return render(request, 'accounts/registration.html', 
        {"error": 1, 
         "username": request.POST['username'],
         "first_name": request.POST['first_name'],
         "last_name": request.POST['last_name'],
         "middle_name": request.POST['last_name'],
         "address": request.POST['address'],
         "email": request.POST['email'],
         "gender": request.POST['gender'],
         "birthdate": request.POST['birthday'],
         "email": request.POST['email'],
         "password": request.POST['password'],
         "confirm_password": request.POST['confirm_password']})

    elif userEmail != None:
        return render(request, 'accounts/registration.html', {"error": 2,
         "username": request.POST['username'],
         "first_name": request.POST['first_name'],
         "last_name": request.POST['last_name'],
         "middle_name": request.POST['last_name'],
         "address": request.POST['address'],
         "email": request.POST['email'],
         "gender": request.POST['gender'],
         "birthdate": request.POST['birthday'],
         "email": request.POST['email'],
         "password": request.POST['password'],
         "confirm_password": request.POST['confirm_password']})

    user.save()

    log = Log()
    log.user_id = User.objects.get(pk=user.id)
    log.description = f'A new account ({user.id} - {user.full_name()}) using username ({user.username}) has been registered.'
    log.save()

    return render(request, 'accounts/registration.html', {"success": 1,
                                                          "username": request.POST['username'],
                                                          "first_name": request.POST['first_name'],
                                                          "last_name": request.POST['last_name'],
                                                          "middle_name": request.POST['last_name'],
                                                          "address": request.POST['address'],
                                                          "email": request.POST['email'],
                                                          "gender": request.POST['gender'],
                                                          "birthdate": request.POST['birthday'],
                                                          "email": request.POST['email'],
                                                          "password": request.POST['password'],
                                                          "confirm_password": request.POST['confirm_password']})

def logout(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    log = Log()
    log.user_id = User.objects.get(pk=logged_user.id)
    log.description = f'{logged_user.full_name()} ({logged_user.id} - {logged_user.username}) has logout.'
    log.save()

    removeSession(request)
    return HttpResponseRedirect(reverse('loginView'))

def setupSession(request, user_id, is_superuser):
    request.session['user_id'] = user_id
    request.session['is_superuser'] = is_superuser

def removeSession(request):
    del request.session['user_id']
    del request.session['is_superuser']
