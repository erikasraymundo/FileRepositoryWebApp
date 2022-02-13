from unicodedata import category
from webbrowser import get
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from category_management.models import Category
from . models import File
from users_management.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files import File as DjangoFile


def index(request,  category_id=0, sort_by=1, query=None, success = 0):
    template_name = 'file_management/index.html'

    if query == None: query = ""
    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "-created_at"

    if (category_id > 0):
            file_list = File.objects.filter(
                Q(name__icontains=query) | 
                Q(category_id__title__icontains=query) |
                Q(user_id__first_name__icontains=query),
                category_id=category_id
            ).order_by(sort_column)
    else:
        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query),
            ).order_by(sort_column)

    return render(request, template_name, 
    {"file_list": file_list,
     "category_selected" : category_id,
     "sort_selected": sort_by,
     "search_value": query,
     "success": success,
     "category_list": Category.objects.all()})

class DetailView(generic.DetailView):
    model = File
    template_name = 'file_management/detail.html'

def openUploadView(request):
    return render(request, 'file_management/upload.html', {"category_list": Category.objects.all()})

def upload(request):

    name = request.POST['name']
    description = request.POST['description']
    cat_id = request.POST['category_id']
    category_id = Category.objects.get(pk=request.POST['category_id'])
    user_id = User.objects.get(pk=1)

    # check if name already exists
    duplicated_list = File.objects.filter(name__iexact=name)
    if not duplicated_list:
        file = File()
        file.name = name
        file.url = request.FILES['file']
        file.description = description
        file.category_id = category_id
        file.user_id = user_id

        try:
            file.save()
            return HttpResponseRedirect(reverse('file-management:success', args={1}))
        except:
            return render(request, 'file_management/upload.html',
                        {"category_list": Category.objects.all(),
                        "name": name,
                        "description": description,
                        "category_id": int(cat_id),
                        "error": 2})  # 2 means general error

    else:
        return render(request, 'file_management/upload.html', 
        {"category_list": Category.objects.all(), 
        "name" : name,
        "description" : description, 
         "category_id": int(cat_id),
         "error": 1}) # 1 means duplicated name

def archive(request):
    return render(request, 'file_management/archive.html')

