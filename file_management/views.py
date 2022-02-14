from unicodedata import category
from webbrowser import get
from django.shortcuts import render
from django.views import generic
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from category_management.models import Category
from . models import File
from activity_log.models import Log
from users_management.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.files import File as DjangoFile
from django.utils import timezone
# Import mimetypes module
import mimetypes
# import os module
import os
# Import HttpResponse module
from django.http.response import HttpResponse
# Import render module
from django.shortcuts import render
from django.http import FileResponse, Http404

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
                category_id=category_id, deleted_at=None
            ).order_by(sort_column)
    else:
        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query), deleted_at=None
            ).order_by(sort_column)

    return render(request, template_name, 
    {"file_list": file_list,
     "category_selected" : category_id,
     "sort_selected": sort_by,
     "search_value": query,
     "success": success,
     "category_list": Category.objects.all()})

def detail(request, file_id):
    template_name = 'file_management/detail.html'
    file = get_object_or_404(File, pk=file_id)
    return render(request, template_name, {"file": file})


def archiveIndex(request,  category_id=0, sort_by=1, query=None, success=0):
    template_name = 'file_management/archive.html'

    if query == None:
        query = ""
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
            Q(user_id__first_name__icontains=query), ~Q(deleted_at=None),
            category_id=category_id, 
        ).order_by(sort_column)
    else:
        file_list = File.objects.filter(
            Q(name__icontains=query) |
            Q(category_id__title__icontains=query) |
            Q(user_id__first_name__icontains=query), ~Q(deleted_at=None)
        ).order_by(sort_column)

    return render(request, template_name,
                  {"file_list": file_list,
                   "category_selected": category_id,
                   "sort_selected": sort_by,
                   "search_value": query,
                   "success": success,
                   "category_list": Category.objects.all()})

def openUploadView(request):
    return render(request, 'file_management/upload.html', 
    {"category_list": Category.objects.all(),
    "error" : 0})

def upload(request):

    name = request.POST['name']
    description = request.POST['description']
    category_id = Category.objects.get(pk=request.POST['category_id'])
    user_id = User.objects.get(pk=1)

    file = File()
    file.name = name
    file.description = description
    file.category_id = category_id
    file.user_id = user_id
    file.url = request.FILES['file']

    try:
        file.save()

        log = Log()
        log.description = f"Uploaded a file ({file.id} - {file.name}) under {file.category_id.title}."
        log.user_id = user_id
        log.save()

        return HttpResponseRedirect(reverse('file-management:success', args={1}))
    except:
        return render(request, 'file_management/upload.html',
            {"category_list": Category.objects.all(),
            "file" : file,
            "error": 1})  # 2 means general error

def openEditView(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    return render(request, 'file_management/edit.html', 
        {"category_list": Category.objects.all(), 
         "file": file,
         "error": 0})

def update(request, file_id):

    name = request.POST['name']
    description = request.POST['description']
    category_id = Category.objects.get(pk=request.POST['category_id'])
    user_id = User.objects.get(pk=1)

    file = File.objects.get(pk=file_id)
    file.name = name
    file.description = description
    file.category_id = category_id
    file.user_id = user_id

    try:
        file.url = request.FILES['file']
    except:
        pass
    try:
        file.save()
        log = Log()
        log.description = f"Updated a file ({file.id} - {file.name}) under {file.category_id.title}."
        log.user_id = user_id
        log.save()
        return HttpResponseRedirect(reverse('file-management:success', args={2}))
    except:
        return render(request, 'file_management/upload.html',
                      {"category_list": Category.objects.all(),
                       "file": file,
                       "error": 1})  # 2

def archive(request, file_id):

    file = get_object_or_404(File, pk=file_id)
    file.deleted_at = timezone.localtime(timezone.now())
    file.save()

    log = Log()
    log.description = f"Archived a file ({file.id} - {file.name})."
    log.user_id = file.user_id
    log.save()

    return HttpResponseRedirect(reverse('file-management:archive-index'))

# def checkDuplicateName(request):
#     # return HttpResponse(1)
#     duplicated_list = File.objects.filter(name__iexact=request.GET['name'])
#     if not duplicated_list:
#         return HttpResponse(0)
#     else:
#         return HttpResponse(1)


def restore(request, file_id):
    file = get_object_or_404(File, pk=file_id)
    file.deleted_at = None
    file.save()

    log = Log()
    log.description = f"Restored a file ({file.id} - {file.name})."
    log.user_id = file.user_id
    log.save()

    return HttpResponseRedirect(reverse('file-management:archive-index'))

def checkDuplicateName(request):
    file_id = int(request.GET['file_id'])
    duplicated_list = File.objects.filter(name__iexact=request.GET['name']).exclude(id=file_id)

    if file_id != 0:
        duplicated_list = File.objects.filter(~Q(id=file_id), name__iexact=request.GET['name'])
    else:
        duplicated_list = File.objects.filter(name__iexact=request.GET['name'])

    if not duplicated_list:
        return HttpResponse(0)
    else:
        return HttpResponse(1)

# Define function to download pdf file using template


def download(request, file_id):

    file = get_object_or_404(File, pk=file_id)
    filename = file.getFileUrl()

    if filename != '':
        # Define Django project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filepath = BASE_DIR + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % file.getNewFileName()
        # Return the response value

        log = Log()
        log.description = f"Downloaded a file ({file.id} - {file.name})."
        log.user_id = file.user_id
        log.save()

        return response
    else:
        # Load the template
        # return HttpResponse("An error has oc!")
        pass


def pdf_view(request, file_id):
    try:
        file = get_object_or_404(File, pk=file_id)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = BASE_DIR + file.getFileUrl()

        return FileResponse(open(filepath, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        # pass
        # return HttpResponse("error")
        raise Http404()
