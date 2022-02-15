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

def printcategories(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    text = c.beginText()
    text.setTextOrigin(inch, inch)
    text.setFont("Helvetica", 12)

    # lines = ["1", "2", "3"]

    
    lines = []


    categories = Category.objects.all()
    for category in categories:
        lines.append(category.title)

    for line in lines:
        text.textLine(line)

    c.drawText(text)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="users.pdf")


def archiveCategory(request):
    return render(request, 'archive.html', {
        'categories' : Category.objects.filter(isArchived = True),
    })

def RestoreCategory(request):
    entry = Category.objects.get(pk = request.POST['ID'])
    entry.isArchived = False
    entry.save()
    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = entry.title + ' has been moved to the active categories from the archive'
    log.save()
    return render(request, 'archive.html', {
        'categories' : Category.objects.filter(isArchived = True),
    })

def UpdateArchivedCategory(request):
    entry = Category.objects.get(pk = request.POST['categoryID'])
    entry.title = request.POST['newCategoryName']
    entry.save()

    log = Log()
    log.user_id = User.objects.get(pk=1)
    log.description = 'Category named ' + Category.objects.get(pk = request.POST['categoryID']).title + ' was renamed to ' + request.POST['newCategoryName']
    log.save()
    return render(request, 'archive.html', {
        'categories' : Category.objects.filter(isArchived = True),
    })