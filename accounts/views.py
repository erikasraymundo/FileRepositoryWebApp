from os import remove
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users_management.models import User
from activity_log.models import Log
import datetime
from django.utils import timezone

def loginView(request, error = 0):
    return render(request, 'accounts/login.html', {"error": error})

# need po itong baguhin
def login(request):

    usernameEmail = request.POST['usernameEmail']
    password = request.POST['password']

    userUsername = User.objects.filter(
        username__iexact=usernameEmail, password=password).first()
    userEmail = User.objects.filter(
        email__iexact=usernameEmail, password=password).first()

    if userUsername != None:
        user = userUsername
        setupSession(request, userUsername.id, userUsername.is_superuser)
    elif userEmail != None:
        user = userEmail
        setupSession(request, userEmail.id, userEmail.is_superuser)
    else:
        return HttpResponseRedirect(reverse('loginViewInvalid', args=[1]))

    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = f'{user.full_name()} ({user.username}) has logged in.'
    log.save()

    return HttpResponseRedirect(reverse('file-management:index'))


def registerView(request, error=0, success=0):
    return render(request, 'accounts/registration.html', {"error": error, "success" : success})

# need po itong baguhin
def register(request):

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
    birthdate = request.POST['birthday']
    user.birthdate = datetime.datetime(
        int(birthdate[6:10]), int(birthdate[0:2]), int(birthdate[3:5]))
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
         "birthdate": birthdate,
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
         "birthdate": birthdate,
         "email": request.POST['email'],
         "password": request.POST['password'],
         "confirm_password": request.POST['confirm_password']})

    user.save()

    log = Log()
    log.user_id = User.objects.get(pk=1)
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
                                                          "birthdate": birthdate,
                                                          "email": request.POST['email'],
                                                          "password": request.POST['password'],
                                                          "confirm_password": request.POST['confirm_password']})

def logout(request):
    removeSession(request)
    return HttpResponseRedirect(reverse('loginView'))

def setupSession(request, user_id, is_superuser):
    request.session['user_id'] = user_id
    request.session['is_superuser'] = is_superuser

def removeSession(request):
    del request.session['user_id']
    del request.session['is_superuser']
