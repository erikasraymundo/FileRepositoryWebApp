from re import template
from django.shortcuts import render
from .models import Category
from django.http import HttpResponse


def categoryManagement(request):
    categoryNames = Category.objects.all()
    return render(request, 'category-management.html', {
        'categories' : categoryNames,
    })

def SaveACategory(request):
    if(request.POST['CategoryInput'] == ''):
        categoryNames = Category.objects.all()
        return render(request, 'category-management.html', {  'categories' : categoryNames, })
    else:
        categoryNames = Category.objects.all()
        for category in categoryNames:
            if(category.title ==  request.POST['CategoryInput']):
                break
        else:
            category = Category()
            category.title = request.POST['CategoryInput']
            category.save()
    
        categoryNames = Category.objects.all()
        return render(request, 'category-management.html', {  'categories' : categoryNames, })