from django.shortcuts import render


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