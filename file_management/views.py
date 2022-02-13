from django.shortcuts import render
from django.views import generic

from category_management.models import Category
from . models import File

<<<<<<< HEAD
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
=======
def base(request):
    return render(request, 'file-management/base.html')

def file_management(request):
    return render(request, 'file-management/file-management.html')

def upload_file(request):
    return render(request, 'file-management/uploadfile.html')

def archive_file(request):
    return render(request, 'file-management/archivefile.html')

def view_file(request):
    return render(request, 'file-management/viewfile.html')
>>>>>>> 9e454f40c9a44a1f345c1009591ce66bf7361312
