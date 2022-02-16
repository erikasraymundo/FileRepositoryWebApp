from re import template
from django.shortcuts import render
from .models import Category
from django.http import HttpResponse
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from category_management.models import Category
from file_management.models import File

from users_management.models import User
from .models import Category
from activity_log.models import Log

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

def categoryManagement(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    categs = Category.objects.filter(isArchived = False)
    nameList = []
    for names in categs:
        nameList.append(names.title)

    
    listOfNotEmptyCategories = []
    categories = Category.objects.all()
    for category1 in categories:
        fileSize = File.objects.filter(category_id = category1.pk)
        for files in fileSize:
            if(files.url.size > 0 ):
                listOfNotEmptyCategories.append(category1.title) if category1.title not in listOfNotEmptyCategories else None

    return render(request, 'category-management.html', {
        'categories' : Category.objects.filter(isArchived = False),
        'user' : logged_user,
        'names' : nameList,
        'undeletable' : listOfNotEmptyCategories 
    })

def AddCategory(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    if(request.POST['CategoryInput'] == ''):
        categoryNames = Category.objects.all()
        return render(request, 'category-management.html', {  'categories' : categoryNames, })
    else:
        categoryNames = Category.objects.all()
        for category in categoryNames:
            if(category.title ==  request.POST['CategoryInput']):
                if(category.isArchived == True):
                    category.isArchived = False
                    category.save()
                    log = Log()
                    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
                    log.description = category.title + ' has been added to active categories from the archive'
                    log.save()
                break

        else:
            category = Category()
            category.title = request.POST['CategoryInput']
            category.save()
            log = Log()
            log.user_id = User.objects.get(pk=  request.session.get('user_id'))
            log.description = category.title + ' has been added to categories'
            log.save()
    return HttpResponseRedirect(reverse('categoryManagement'))

def DeleteCategory(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    entry = Category.objects.get(pk = request.POST['ID'])
    entry.isArchived =True
    entry.save()
    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = entry.title + ' has been moved to the archived categories'
    log.save()
    return HttpResponseRedirect(reverse('categoryManagement'))

def UpdateCategory(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    entry = Category.objects.get(pk = request.POST['categoryID'])
    entry.title = request.POST['newCategoryName']
    entry.save()

    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = 'Category named ' + Category.objects.get(pk = request.POST['categoryID']).title + ' was renamed to ' + request.POST['newCategoryName']
    log.save()
    return HttpResponseRedirect(reverse('categoryManagement'))

def archiveCategory(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))
    
    return render(request, 'archive.html', {
        'categories' : Category.objects.filter(isArchived = True),
        'user' : logged_user
    })

def RestoreCategory(request):
    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    entry = Category.objects.get(pk = request.POST['ID'])
    entry.isArchived = False
    entry.save()
    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = entry.title + ' has been moved to the active categories from the archive'
    log.save()

    return HttpResponseRedirect(reverse('archiveCategory'))

def UpdateArchivedCategory(request):

    try:
        session_user_id = request.session.get('user_id')
        logged_user = User.objects.get(pk=session_user_id)
    except:
        return HttpResponseRedirect(reverse('index'))

    entry = Category.objects.get(pk = request.POST['categoryID'])
    entry.title = request.POST['newCategoryName']
    entry.save()

    log = Log()
    log.user_id = User.objects.get(pk=  request.session.get('user_id'))
    log.description = 'Category named ' + Category.objects.get(pk = request.POST['categoryID']).title + ' was renamed to ' + request.POST['newCategoryName']
    log.save()

    return HttpResponseRedirect(reverse('archiveCategory'))