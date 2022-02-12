from django.shortcuts import render


def file_management(request):
    return render(request, 'file-management.html')