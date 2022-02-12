from django.shortcuts import render


def file_management(request):
    return render(request, 'file-management.html')

def upload_file(request):
    return render(request, 'uploadfile.html')

def archive_file(request):
    return render(request, 'archivefile.html')

def view_file(request):
    return render(request, 'viewfile.html')