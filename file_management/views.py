from unicodedata import category
from django.shortcuts import render
from django.views import generic

from category_management.models import Category
from . models import File


def index(request,  category_id=0, sort_by=1):
    template_name = 'file_management/index.html'

    sort_column = "name"

    if (sort_by == 2):
        sort_column = "category_id__title"
    elif (sort_by == 3):
        sort_column = "user_id__first_name"
    elif (sort_by == 4):
        sort_column = "created_at"

    if (category_id > 0):
        file_list = File.objects.filter(category_id=category_id).order_by(sort_column)
    else:
        file_list = File.objects.filter().order_by(sort_column)

    return render(request, template_name, 
    {"file_list": file_list,
     "category_selected" : category_id,
     "sort_selected": sort_by,
     "category_list": Category.objects.all()})

class DetailView(generic.DetailView):
    model = File
    template_name = 'file_management/detail.html'

def upload(request):
    return render(request, 'file_management/upload.html')

def archive(request):
    return render(request, 'file_management/archive.html')
