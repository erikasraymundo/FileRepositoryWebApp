from os import remove
from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users_management.models import User

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
        setupSession(request, userUsername.id, userUsername.is_superuser)
    elif userEmail != None:
        setupSession(request, userEmail.id, userEmail.is_superuser)
    else:
        return HttpResponseRedirect(reverse('loginViewInvalid', args=[1]))

    return HttpResponseRedirect(reverse('file-management:index'))


def registerView(request, error=0):
    return render(request, 'accounts/registration.html', {"error": error})

# need po itong baguhin
def register(request):

    user = User()
    user.username = request.POST['username']
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.middle_name = request.POST['middle_name']
    user.address = request.POST['address']
    user.email = request.POST['email']
    user.gender = request.POST['group']
    birthdate = request.POST['birthday']
    user.birthdate = datetime.datetime(int(birthdate[6:10]), int(birthdate[0:2]), int(birthdate[3:5]))
    user.date_joined =  timezone.now()
    user.is_superuser = False
    user.is_staff = False
    user.user_type = 1
    user.save()

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
