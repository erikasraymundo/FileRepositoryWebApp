from django.shortcuts import render
from django.views import generic

from category_management.models import Category
from . models import File

class IndexView(generic.ListView):
    template_name = 'file_management/index.html'
    context_object_name = 'file_list'

    def get_queryset(self):
        return File.objects.order_by("-id")

def index(request):
    template_name = 'file_management/index.html'
    return render(request, template_name, 
    {"file_list": File.objects.order_by("-id"),
     "category_list": Category.objects.all()})

class DetailView(generic.DetailView):
    model = File
    template_name = 'file_management/detail.html'

def upload(request):
    return render(request, 'file_management/upload.html')

def archive(request):
    return render(request, 'file_management/archive.html')