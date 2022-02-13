from re import template
from django.shortcuts import render

from users_management.models import User
from .models import Category
from activity_log.models import Log

def categoryManagement(request):
    return render(request, 'category-management.html', {
        'categories' : Category.objects.filter(isArchived = False),
    })

def AddCategory(request):
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
                    log.user_id = User.objects.get(pk=1)
                    log.description = category.title + ' has been added to active categories from the archive'
                    log.save()
                break

        else:
            category = Category()
            category.title = request.POST['CategoryInput']
            category.save()
            log = Log()
            log.user_id = User.objects.get(pk=1)
            log.description = category.title + ' has been added to categories'
            log.save()
    return render(request, 'category-management.html', {
        'categories' : Category.objects.filter(isArchived = False),
    })

def DeleteCategory(request):
    entry = Category.objects.get(pk = request.POST['ID'])
    entry.isArchived =True
    entry.save()
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = entry.title + ' has been moved to the archived categories'
    log.save()
    return render(request, 'category-management.html', {
        'categories' : Category.objects.filter(isArchived = False),
    })

def UpdateCategory(request):
    entry = Category.objects.get(pk = request.POST['categoryID'])
    entry.title = request.POST['newCategoryName']
    entry.save()

    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Category named ' + Category.objects.get(pk = request.POST['categoryID']).title + ' was renamed to ' + request.POST['newCategoryName']
    log.save()
    return render(request, 'category-management.html', {
        'categories' : Category.objects.filter(isArchived = False),
    })